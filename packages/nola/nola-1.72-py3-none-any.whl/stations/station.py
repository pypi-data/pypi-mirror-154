import json
import boto3
import logging
import pandas as pd
import os
os.environ['MPLCONFIGDIR'] = "/tmp"
import matplotlib.pyplot as plt
import math
from io import BytesIO
from datetime import datetime
import statistics
from botocore.exceptions import ClientError
import numbers
from matplotlib.colors import LogNorm, Normalize, SymLogNorm


def days_diff(d1, d2):
    """
    Returns days between dates:  d2 - d1

    :param d1:
    :param d2:
    :return:
    """
    print("days_diff: formatting dates")
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    print("days_diff: subtracting dates")
    return (d2 - d1).days


def release_obsvs(release):
    return release.index[release.notna()].tolist()


def restatement_estimatator(old_release, new_release, phi=.5):
    obsv = release_obsvs(new_release)
    restated_num = sum(old_release[obsv] != new_release.loc[obsv])
    obsv_num = len(obsv)
    if obsv_num > 0:
        perc_restated = restated_num / obsv_num
        return perc_restated > phi, perc_restated
    else:
        return False, 0

def retroactive_changes(data, phi=.5):
    dta = data.dropna(axis='columns', how='all')
    cols = dta.columns
    num_restated = 0
    restatements = []
    dct = {}

    for old, new in zip(cols[:-1], cols[1:]):
        restated, __ = restatement_estimatator(dta[old], dta[new], phi)
        num_restated += restated
        dct[new] = {"ConsistencyRetroactiveChange": int(restated)}

        if restated:
            restatements.append((old, new))

    return num_restated, restatements, pd.DataFrame.from_dict(dct)


def accuracyMetric(target, reported):
    """return Absolute error"""
    return abs(target - reported)


def accuracy_metrics(vals, truth_val, expected_dt):
    """
    normalized accuracy = average( 1 - acc_i / truth_i) where x_i is not null

    :param vals:
    :param expected_dt:
    :param truth_val:
    :return: dict
    """
    accs = [accuracyMetric(truth_val, val) for val in vals[vals.notna()]]

    orig_acc = None
    avg = None
    std = None
    final_acc = None
    normalized_acc = None

    if len(accs) > 1:
        std = statistics.stdev(accs)
        avg = sum(accs) / len(accs)
        orig_acc = accs[0]
        final_acc = accs[-1]
    elif len(accs) == 1:
        avg = accs[0]
        orig_acc = accs[0]
        final_acc = accs[0]

    if truth_val != 0:
        normalized_acc = (1 / len(accs)) * (sum([1 - (acc / truth_val) for acc in accs]))

    return {
        "OriginalAccuracy": orig_acc,
        "AverageAccuracy": avg,
        "AccuracySTDev": std,
        "FinalAccuracy": final_acc,
        "NormalizedAccuracy": normalized_acc
    }


def completeness_metric(series, truth_df, expected_df, *args, **kwargs):
    """
    Returns percent of an update that includes previous values

    :param vals:
    :param expected_dt:
    :param truth_val:
    :return:
    """
    # check that there is an update for all the expected less than or equal to this
    expected_vals = expected_df[expected_df.iloc[:, 0] < series.name].index
    not_na = series[series.notna()]
    num_missing = len([each for each in expected_vals if each not in not_na.index])
    if len(expected_vals) > 0:
        return {"Completeness": 1 - (num_missing / len(expected_vals))}
    else:
        return {"Completeness": None}


def time_till_metrics(vals, truth_val, expected_dt):
    """

    :param vals: pandas Series object
    :param expected_dt:
    :param truth_val:
    :return:
    """
    # to accommodate not updated dates
    vals_not_na = vals[vals.notna()]

    # ------Time Till Reported------- #
    # first date updated
    first_reported = vals_not_na.index[0]

    # ------Time Till Accurate------- #
    # Else the final value was correct, and we need to find the last date for which it changed

    # changes between updates; [NaN, val1-val0, ...]
    diffs = [each for each in vals_not_na.diff()]

    # Find the dates at which the value changed
    change_dates = [ind for ind, dff in zip(vals_not_na.index, diffs) if dff != 0]
    time_till_accurate = days_diff(expected_dt, change_dates[-1])

    # If final value was not correct
    if truth_val != vals_not_na[-1]:
        time_till_accurate = 2 * days_diff(expected_dt,
                                           vals.index[-1])  # should this be something like more days than have elapsed?
    return {
        "TimeTillReported": days_diff(expected_dt, first_reported),
        "TimeTillAccurate": time_till_accurate
    }


def validity_nondecreasing_step(series, truth_df, expected_df, *args, **kwargs):
    """
    - 1 + (2/ (1 + e^(- 5 * num increasing updates / possible updates)
    :param series:
    :param truth_df:
    :param expected_df:
    :param args:
    :param kwargs:
    :return:
    """
    truth_max = truth_df[expected_df.index < series.name].iloc[:, 0].max()
    num_expected_updates = len(expected_df[expected_df.index < series.name].iloc[:, 0].unique())
    denom = (min(num_expected_updates, truth_max) / 5)  # min represents the possible updates

    if denom == 0:
        return None

    coef = -1 / denom
    num_increasing_updates = len(series[series.diff() > 0])

    return -1 + 2 / (1 + math.exp(coef * num_increasing_updates))


def validity_nondecreasing_smoothness(series, truth_df, expected_df, *args, **kwargs):
    """
    Assumes series is of nondecreasing observations by increasing dates

    :param series:
    :param truth_df:
    :param expected_df:
    :param args:
    :param kwargs:
    :return:
    """
    orig_diffs = series.diff()  # nan, 2
    rises = [abs(diff) for diff in orig_diffs if diff > 0]  # 2
    inds = [ind for ind, diff in enumerate(orig_diffs) if diff > 0]  # 2020-03-28

    if len(inds) == 0:
        return 0

    runs = [inds[0]]  # 2020-03-28
    if len(inds) > 1:
        runs = runs + [abs(ind2 - ind1) for ind1, ind2 in zip(inds[:-1], inds[1:])]

    # last observation updated (max dt not na)
    obsvs = series[series.notna()]
    # max_date = obsvs.index[-1]
    max_val = obsvs.iloc[-1]  # 6
    num_expected_dates = expected_df[expected_df.iloc[:, 0] < series.name].shape[0]  # 2
    total_area = max_val * num_expected_dates  # 6x2
    covered_area = sum([rise * run for rise, run in zip(rises, runs)])  # sum([]
    if total_area > 0:
        return 1 - (covered_area / total_area)
    else:
        return None


def validity_nondecreasing(series, *args, **kwargs):
    """
    Percent of changes in sequential observations that increase (within a release)
    1 - (num of changes that decrease) / (number of changes)
    where a change is a reported value which is not equal to the previous observation
    """
    num_decreasing_updates = len([each for each in series[series.notna()].diff() if each < 0])
    num_updates = len([each for each in series[series.notna()].diff() if each != 0])
    if num_updates > 2:
        return 1 - (num_decreasing_updates / (num_updates - 1))
    else:
        return 1


def consistency_percent_of_release_changes_increasing(series, truth_df, expected_df, *args, **kwargs):
    """
    Returns the percent of total abs(changes) in a release that are positive
    Attempts to capture nonretroactive change impact
    :param series: 
    :param truth_df: 
    :param expected_df: 
    :param args: 
    :param kwargs: 
    :return: 
    """
    # |sum of increases| / |sum of absolute changes|
    decreases = sum([abs(diff) for diff in series.diff().dropna() if diff < 0])
    changes = sum([abs(diff) for diff in series.diff().dropna()])
    if changes > 0:
        return decreases / changes
    else:
        return None


def consistency_between_releases(data_df, truth_df, expected_df):
    """
    Returns a pandas dataframe of percent of release restated from prior release 
    :param data_df: 
    :param truth_df: 
    :param expected_df: 
    :return: 
    """
    releases = data_df.columns
    dct = {}
    last_non_null = None

    for prior, post in zip(releases[:-1], releases[1:]):

        if len(data_df[prior].notna()) > 0:
            last_non_null = data_df[prior]
        
        post_nonnulls = data_df[post].notna()
        
        diff = data_df[post][post_nonnulls] - last_non_null[post_nonnulls]

        if len(diff) > 0:
            dct[post] = {"ConsistencyPercentUpdated": len(diff[diff != 0]) / len(diff)}
        else:
            dct[post] = None

    return pd.DataFrame.from_dict(dct)


# ----------------------------------------------#
# -------- Data Quality Dimensions--------------#
# ----------------------------------------------#

def apply_to_observations(func):
    """
    Execute a function over the values reported for an observation across releases

    :param func:
    :return: func
    """

    def over_observations(data_df, truth_df, expected_df, *args, **kwargs):
        dct = {}

        for obsv, vals in data_df.iterrows():

            not_na = vals[vals.notna()]
            if len(not_na) == 0:
                dct[obsv] = {}

            else:
                truth_val = truth_df.loc[obsv][0]
                expected_dt = expected_df.loc[obsv][0]

                dct[obsv] = func(vals, truth_val, expected_dt, *args, **kwargs)

        return pd.DataFrame.from_dict(dct, orient='index')

    return over_observations


def apply_to_releases(func):
    """
    Execute a function over the values sequentially across observations in a given release

    :param func:
    :return: func
    """

    def over_releases(data_df, truth_df, expected_df, *args, **kwargs):
        dct = {}

        for update, series in data_df.iteritems():

            not_na = series[series.notna()]
            if len(not_na) == 0:
                dct[update] = None

            else:
                dct[update] = func(series, truth_df, expected_df, *args, **kwargs)

        return pd.DataFrame.from_dict(dct, orient='columns')

    return over_releases


def timeliness(data_df, truth_df, expected_df):
    """

    :param data_df:
    :param truth_df:
    :param expected_df:
    :return:
    """
    func = apply_to_observations(time_till_metrics)
    return func(data_df, truth_df, expected_df)


def accuracy(data_df, truth_df, expected_df):
    """

    :type data_df: object
    :param data_df:
    :param truth_df:
    :param expected_df:
    :return:pandas dataframe
    """

    func = apply_to_observations(accuracy_metrics)
    return func(data_df, truth_df, expected_df)


def validity(data_df, truth_df, expected_df):
    def validity_metrics(series, truth_df, expected_df):
        return {
            "ValidityNondecreasingSmoothness":
                validity_nondecreasing_smoothness(series, truth_df, expected_df),
            "ValidityNondecreasingUpdates":
                validity_nondecreasing(series, truth_df, expected_df),
            "ValidityNondecreasingStep":
                validity_nondecreasing_step(series, truth_df, expected_df),
        }

    func = apply_to_releases(validity_metrics)
    return func(data_df, truth_df, expected_df)


def consistency(data_df, truth_df, expected_df):
    def consistency_metrics(series, truth_df, expected_df):
        return {
            "ConsistencyNondecreasingPercentRestatement":
                consistency_percent_of_release_changes_increasing(series, truth_df, expected_df)
        }

    func = apply_to_releases(consistency_metrics)
    df1 = func(data_df, truth_df, expected_df)
    print(type(df1))
    print(df1.shape)
    df2 = consistency_between_releases(data_df, truth_df, expected_df)
    print(type(df2))
    print(df2.shape)
    __, __, df3 = retroactive_changes(data_df)
    return pd.concat([df1, df2, df3])


def completeness(data_df, truth_df, expected_df):
    func = apply_to_releases(completeness_metric)
    return func(data_df, truth_df, expected_df)


def basic_stats(data_df, truth_df, expected_df):
    desc = truth_df.describe().T
    desc.columns = [f'truth_{each}' for each in desc.columns]
    return desc


# ----------------------------------------------#
# -------------- AWS Management-----------------#
# ----------------------------------------------#

def save_plt_to_s3(plt, bucket, key, format='png', **kwargs):
    img_data = BytesIO()
    plt.savefig(img_data, format=format)
    img_data.seek(0)

    s3 = boto3.resource('s3', **kwargs)
    bucket = s3.Bucket(bucket)
    print(f'Attempting to put image {key} in {bucket}')
    resp = bucket.put_object(Body=img_data, ContentType='image/png', Key=key)
    print(f'Successfully put image {key} in {bucket}')
    return resp


def df_from_s3_csv(bucket, key, **kwargs):
    """

    :param s3_client: a boto3 client object for s3
    :param bucket: str
    :param key: str
    :return: pandas dataframe
    """
    s3_client = boto3.client('s3', **kwargs)
    logging.info(f'Attempting to read S3 object {key}')
    print(f'Attempting to read S3 object {key} in {bucket}')
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    print(f'Successfully read S3 object {key} in {bucket}')
    logging.info(f'Successfully read S3 object {key}')
    df = pd.read_csv(obj['Body'], sep=',', index_col=0)
    return df


def df_to_s3_csv(bucket, key, df, **kwargs):
    """

    :param s3_client: boto3 client object for s3
    :param bucket: str
    :param key: str
    :param df: pandas dataframe
    :return: True
    """
    print("Connecting to S3")
    s3_client = boto3.client('s3', **kwargs)

    print("Writing BytesIO")
    with BytesIO() as csv_buffer:
        df.to_csv(csv_buffer)
        print(f'Attempting to put object to bucket {bucket} at key {key}')
        response = s3_client.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    return status


def send_sqs_message(to_sqs_url, msg_body, region_name, **kwargs):
    """

    :param to_sqs_url: str
    :param msg_body: dictionary
    :param region_name: str
    :return:
    """
    sqs_client = boto3.client('sqs', region_name=region_name, **kwargs)

    try:
        msg = sqs_client.send_message(QueueUrl=to_sqs_url,
                                      MessageBody=json.dumps(msg_body))
        return msg

    except ClientError as e:
        logging.error(e)
        return None

def make_key(file, path=''):
    if path == "":
        return file
    else:
        return "/".join([path, file])


# ----------------------------------------------#
# -------------- Nodes -------------------------#
# ----------------------------------------------#
def metric_node(
        event,
        context,
        to_sqs_url,
        region_name,
        to_bucket,
        to_key,
        func="accuracy"
):
    """
        The structure of a processing station: receive, load, do, save, send

    Load a pandas dataframe from the buck/key referenced in the triggering event
    Execute func on the dataframe which must return a df
    Put the df into to_bucket/key
    Send message to to_sqs_url

    :param event:
    :param context:
    :param to_sqs_url: str
    :param region_name: str
    :param to_bucket: str
    :param to_key: str
    :param func: func(data_df, truth_df, expected_df) returns a pandas df
    :return:
    """
    funcs_mapping = {
        "stats": basic_stats,
        "accuracy": accuracy,
        "timeliness": timeliness,
        "validity": validity,
        "consistency": consistency,
        "completeness": completeness
    }

    logging.getLogger().setLevel(logging.INFO)
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(levelname)s: %(asctime)s: %(message)s')

    body = event["Records"][0]["body"]
    if isinstance(body, str):
        body = json.loads(body)

    from_bucket = body['bucket']
    path, data_file, truth_file, expected_file = "", "data.csv", "truth.csv", "expected_update.csv"
    if 'path' in body:
        path = body['path']
    if 'data_file' in body:
        data_file = body['data_file']
    if 'truth_file' in body:
        truth_file = body['truth_file']
    if 'expected_file' in body:
        expected_file = body['expected_file']

    completed_stations = [each for each in body['completed_stations']]

    data_df = df_from_s3_csv(from_bucket, make_key(data_file, path))
    truth_df = df_from_s3_csv(from_bucket, make_key(truth_file, path))
    expected_df = df_from_s3_csv(from_bucket, make_key(expected_file, path))

    finished_df = funcs_mapping[func](data_df, truth_df, expected_df)

    status = df_to_s3_csv(bucket=to_bucket, key=make_key(to_key, path), df=finished_df)

    if status == 200:
        logging.info(f'Successful S3 put_object response')

    else:
        logging.info(f'Unsuccessful S3 put_object response - {status}')

    completed_stations.append(context.function_name)

    message = {
        'bucket': from_bucket,
        'path': path,
        'data_file': data_file,
        'truth_file': truth_file,
        'expected_file': expected_file,
        'completed_stations': completed_stations
    }

    msg = send_sqs_message(to_sqs_url, message, region_name)

    if msg is not None:
        logging.info(f'Sent SQS message ID: {msg["MessageId"]}')

    return {
        'statusCode': status,
        'body': message
    }


def summary_node(
        event,
        context,
        to_sqs_url,
        region_name,
        from_bucket,
        to_bucket,
        to_key
):
    """
     Summarize the Data Quality Dimensions

    Load a pandas dataframe from the buck/key referenced in the triggering event
    Execute func on the dataframe which must return a df
    Put the df into to_bucket/key
    Send message to to_sqs_url


    """
    dims_files = [
        "timeliness.csv",
        "accuracy.csv",
        "validity.csv",
        "completeness.csv",
        "consistency.csv"
    ]

    body = event["Records"][0]["body"]
    if isinstance(body, str):
        body = json.loads(body)

    path, data_file, truth_file, expected_file = "", "data.csv", "truth.csv", "expected_update.csv"
    if 'path' in body:
        path = body['path']
    if 'data_file' in body:
        data_file = body['data_file']
    if 'truth_file' in body:
        truth_file = body['truth_file']
    if 'expected_file' in body:
        expected_file = body['expected_file']

    completed_stations = [each for each in body['completed_stations']]

    dfs = []
    transpose = ["validity.csv", "consistency.csv", "completeness.csv"]

    for from_key in dims_files:
        df = df_from_s3_csv(from_bucket, make_key(from_key, path))

        if from_key in transpose:
            df = df.T

        desc_cols = ['mean', '50%', 'std']
        df_desc = df.describe()
        df_desc = df_desc.loc[desc_cols]
        df_desc.index = ['mean', 'median', 'std']
        df_desc = df_desc.T
        df_desc["coef_var"] = df_desc['std'] / df_desc['mean']
        kurtosis = df.kurtosis()
        df_desc = pd.concat([df_desc, kurtosis], axis=1)
        df_desc.rename({0: "kurtosis"}, inplace=True, axis=1)
        dfs.append(df_desc)

    finished_df = pd.concat(dfs)

    status = df_to_s3_csv(bucket=to_bucket, key=make_key(to_key, path), df=finished_df)

    flattened = finished_df.unstack().to_frame().sort_index(level=1).T
    flattened.columns = flattened.columns.map('_'.join)
    flattened.index = ['0']

    stats = df_from_s3_csv(from_bucket, make_key("stats.csv", path))
    stats.index = ['0']
    flattened = pd.concat([stats, flattened], axis=1)
    # concat flattened to stats

    status = df_to_s3_csv(bucket=to_bucket, key=make_key(f'flattened_{to_key}', path), df=flattened)

    completed_stations.append(context.function_name)

    message = {
        'bucket': from_bucket,
        'path': path,
        'data_file': data_file,
        'truth_file': truth_file,
        'expected_file': expected_file,
        'summary_file': to_key,
        'completed_stations': completed_stations
    }

    msg = send_sqs_message(to_sqs_url, message, region_name)

    if msg is not None:
        logging.info(f'Sent SQS message ID: {msg["MessageId"]}')

    return {
        'statusCode': status,
        'body': message
    }


def plot_node(
        event,
        context,
        to_sqs_url,
        region_name,
        from_bucket,
        to_bucket,
        to_key
):
    """

    :param event:
    :param context:
    :param to_sqs_url:
    :param region_name:
    :param from_bucket:
    :param to_bucket:
    :param to_key:
    :return:
    """
    body = event["Records"][0]["body"]
    if isinstance(body, str):
        body = json.loads(body)

    from_bucket = body['bucket']
    path, data_file, truth_file, expected_file = "", "data.csv", "truth.csv", "expected_update.csv"
    summary_file = 'summary.csv'
    prepared_bucket = 'prepared-data'
    evaluated_bucket = 'evaluated-data'
    if 'path' in body:
        path = body['path']
    if 'data_file' in body:
        data_file = body['data_file']
    if 'truth_file' in body:
        truth_file = body['truth_file']
    if 'expected_file' in body:
        expected_file = body['expected_file']
    if 'summary_file' in body:
        summary_file = body['summary_file']

    completed_stations = [each for each in body['completed_stations']]

    print('Clearing Image')
    plt.close()
    print('Cleared Image')
    # plot truth data

    print("Creating Line Plot of Truth Values")
    truth_df = df_from_s3_csv(prepared_bucket, make_key(truth_file, path))
    image_name = 'truth_plot.png'
    fancy_path = path.replace("/", ": ").replace("_", " ")
    truth_df.iloc[:, -1].plot(kind="line", figsize=(14, 14))
    plt.title(fancy_path, fontsize=20)
    plt.xticks(rotation=45, ha='right')
    save_plt_to_s3(plt, to_bucket, make_key(image_name, path), format='png')

    print('Clearing Image')
    plt.close()
    print('Cleared Image')

    # plot heatmap
    print("Creating Heatmap of Data")
    image_name = 'data_heatmap_lognorm.png'
    data_df = df_from_s3_csv(prepared_bucket, make_key(data_file, path))
    plt.figure(figsize=(15, 15))
    plt.pcolormesh(data_df, norm=LogNorm(vmin=1))
    len_ind = len(data_df.index)
    len_cols = len(data_df.columns)
    ynum = max(len_ind // 10, 1)
    xnum = max(len_cols // 5, 1)
    yticks = [each for each in range(len_ind) if each % ynum == 0]
    xticks = [each for each in range(len_cols) if each % xnum == 0]
    plt.yticks(ticks=[y + .5 for y in yticks], labels=data_df.index[yticks])
    plt.xticks(ticks=[x + .5 for x in xticks], labels=data_df.columns[xticks], rotation=45, ha='right')
    plt.colorbar()
    plt.title(f'{fancy_path}', fontsize=15)
    plt.xlabel('Update', fontsize=15)
    plt.ylabel('Reporting Date (Subject)', fontsize=15)
    save_plt_to_s3(plt, to_bucket, make_key(image_name, path), format='png')

    print('Creating non-norm heatmap Heatmap')
    image_name = 'data_heatmap.png'
    plt.pcolormesh(data_df)
    plt.colorbar()
    save_plt_to_s3(plt, to_bucket, make_key(image_name, path), format='png')

    print('Creating non-norm heatmap Heatmap normalized')
    image_name = 'data_heatmap_normalized.png'
    plt.pcolormesh(data_df, norm=Normalize())
    plt.colorbar()
    save_plt_to_s3(plt, to_bucket, make_key(image_name, path), format='png')
    print('Clearing Heatmaps')
    plt.close()
    print('Cleared Heatmap')

    print("Creating Heatmap of Differences of Releases")
    image_name = 'data_diff_heatmap.png'
    plt.figure(figsize=(15, 15))
    plt.pcolormesh(data_df.diff(axis=1), norm=SymLogNorm(linthresh=0.5))
    len_ind = len(data_df.index)
    len_cols = len(data_df.columns)
    ynum = max(len_ind // 10, 1)
    xnum = max(len_cols // 5, 1)
    yticks = [each for each in range(len_ind) if each % ynum == 0]
    xticks = [each for each in range(len_cols) if each % xnum == 0]
    plt.yticks(ticks=[y + .5 for y in yticks], labels=data_df.index[yticks])
    plt.xticks(ticks=[x + .5 for x in xticks], labels=data_df.columns[xticks], rotation=45, ha='right')
    plt.colorbar()
    plt.title(f'{fancy_path} Release Differences', fontsize=15)
    plt.xlabel('Update', fontsize=15)
    plt.ylabel('Reporting Date (Subject)', fontsize=15)
    save_plt_to_s3(plt, to_bucket, make_key(image_name, path), format='png')

    print('Clearing Heatmap of Differences ')
    plt.close()
    print('Cleared Heatmap of Differences ')

    print("Creating Heatmap of Differences within Releases")
    image_name = 'data_diff_heatmap_win_release.png'
    plt.figure(figsize=(15, 15))
    plt.pcolormesh(data_df.diff(axis=0), norm=SymLogNorm(linthresh=0.5))
    len_ind = len(data_df.index)
    len_cols = len(data_df.columns)
    ynum = max(len_ind // 10, 1)
    xnum = max(len_cols // 5, 1)
    yticks = [each for each in range(len_ind) if each % ynum == 0]
    xticks = [each for each in range(len_cols) if each % xnum == 0]
    plt.yticks(ticks=[y + .5 for y in yticks], labels=data_df.index[yticks])
    plt.xticks(ticks=[x + .5 for x in xticks], labels=data_df.columns[xticks], rotation=45, ha='right')
    plt.colorbar()
    plt.title(f'{fancy_path} Release Differences', fontsize=15)
    plt.xlabel('Update', fontsize=15)
    plt.ylabel('Reporting Date (Subject)', fontsize=15)
    save_plt_to_s3(plt, to_bucket, make_key(image_name, path), format='png')

    print('Clearing Heatmap of Differences ')
    plt.close()
    print('Cleared Heatmap of Differences ')

    # create an image of the table
    print("Creating Summary Table")
    image_name = 'summary_table.png'
    summary_df = df_from_s3_csv(evaluated_bucket, make_key(summary_file, path))

    def shorten(x):
        if isinstance(x, numbers.Number):
            return round(x, 3)
        else:
            return x

    column_headers = summary_df.columns
    row_headers = summary_df.index

    cell_text = []
    for __, row in summary_df.iterrows():
        cell_text.append([f'{shorten(x)}' for x in row])

    plt.figure(linewidth=2,
               figsize=(15, 7)
               )
    plt.tight_layout()
    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                          rowLabels=row_headers,
                          rowLoc='right',
                          colLabels=column_headers,
                          loc='center'
                          )
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(12)
    the_table.scale(2, 2)
    the_table.auto_set_column_width(col=list(range(len(summary_df.columns))))

    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # Hide axes border
    plt.box(on=None)
    # Add title
    plt.suptitle(fancy_path, fontsize=20)
    plt.draw()
    save_plt_to_s3(plt, to_bucket, make_key(image_name, path), format='png')

    print('Clearing Image')
    plt.close()
    print('Cleared Image')

    return {
        'statusCode': 'temp_status',
        'body': 'done'
    }