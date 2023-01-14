import cv2
from time import time
from minio import Minio
import base64
import io
import numpy as np

def video_processing(video_name, video_path):
    result_file_path = '/tmp/output-'+ video_name

    video = cv2.VideoCapture(video_path)

    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_file_path, fourcc, 20.0, (width, height))

    start = time()
    while(video.isOpened()):
        ret, frame = video.read()

        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            is_success, buff = cv2.imencode(".jpg", gray_frame)
            io_buf = io.BytesIO(buff)
            gray_frame = cv2.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)
            out.write(gray_frame)
        else:
            break

    latency = time() - start

    video.release()
    out.release()
    return latency, result_file_path

def main(params):
    endpoint = params['endpoint']
    access_key = params['access_key']
    secret_key = params['secret_key']
    bucket = params['bucket']

    minio_client = Minio(endpoint=endpoint,
                     access_key=access_key,
                     secret_key=secret_key,
                     secure=False)
    found = minio_client.bucket_exists(bucket)
    if not found:
        print("Bucket '%s' does not exist" %bucket)

    video_name = params['video']
    video_path = '/tmp/' + video_name

    headers={"Cookie": 'session-id=138-4794293-6479124; session-id-time=2082787201l; i18n-prefs=USD; lc-main=zh_CN; sp-cdn="L5Z9:MO"; ubid-main=130-4109747-4138841; session-token="9NVs7ra4+oOM8ITlu09mN8iBgb/CKEi8gxg4r78yEu3ZjT9Ms5HMS1l0oUWslLaXdfSmgQupYfWQa92a5TvqYBh75wr9MQEFrW2hEqGfWsGDUJG8Bts0dOf3Yfl8VHuwo3Drc/BJf2oQDffzFM3x8S4yj3PDUnx8Yn8+fkeeEeyx0sE2KzQPddFQSURI2Ugl/EiymHIEMpUkQ6HWOhictyPlFYRrW4PlOy0WN/nJEu8="; aws-priv=eyJ2IjoxLCJldSI6MCwic3QiOjB9; aws_lang=cn; aws-target-data=%7B%22support%22%3A%221%22%7D; AMCVS_7742037254C95E840A4C98A6%40AdobeOrg=1; s_cc=true; _mkto_trk=id:112-TZM-766&token:_mch-aws.amazon.com-1668414076926-21645; aws-mkto-trk=id%3A112-TZM-766%26token%3A_mch-aws.amazon.com-1668414076926-21645; aws-target-visitor-id=1668135652584-839458.38_0; aws-vid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwaWQiOiIyMjAxZjE0MS1jMjNhLTQxNzktOWViOC05OTM1ZTE0YzRkYWMiLCJ1YXQiOjE2Njg4MjUzNjgxOTcsImV4cCI6MTcwMDM2MTM2ODE5NywicHZkIjoiYXdzLmFtYXpvbi5jb20ifQ.4i9ozO95s2gGPlL09DEzWa4WwFW-khRA4eq3LfCLv0w; aws-ubid-main=472-5270171-7532740; aws-account-data=%7B%22marketplaceGroup%22%3A%22AWS%22%7D; awsc-uh-opt-in=; regStatus=registered; awsc-rac=BAH00|CGK00|CPT00|DXB00|HKG11|MXP00|ZAZ00|ZRH00@1669006481779; noflush_Region=us-east-1; noflush_locale=zh-CN; awsccc=eyJlIjoxLCJwIjoxLCJmIjoxLCJhIjoxLCJpIjoiMWVkNDIzOTEtYTk4ZS00ZGJkLTliMGEtNTk0NWJhNDFhMGJlIiwidiI6IjEifQ==; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJ1cy1lYXN0LTEiLCJhbGciOiJFUzM4NCIsImtpZCI6ImFmY2M3ZGEzLWQyNWMtNGNmMC04ZTdkLWEzOGMyOTlhNTUxNSJ9.eyJzdWIiOiIiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoiRG9LblJlTUtNa0ViRW84VDFRV0ZZelMwZnJyKzZveHl1M3Z2TG5tMVZwbz0iLCJhcm4iOiJhcm46YXdzOmlhbTo6ODAxNDIyNzk1OTA4OnJvb3QiLCJ1c2VybmFtZSI6InNoZW5iZW4ifQ.5YxALK0J1ZeQViPIzp_qx3nPQJnlKdWkXK7x6QQRRql7IWwMXCwH6IF9TYi_S-gvKk9Rm_CRaJZ4Od18Xe8BvPh5GYabeeCzu1O8Rsi3TdNEenBFShQPFJxXLHmyYqYn; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A801422795908%3Aroot%22%2C%22alias%22%3A%22%22%2C%22username%22%3A%22shenben%22%2C%22keybase%22%3A%22DoKnReMKMkEbEo8T1QWFYzS0frr%2B6oxyu3vvLnm1Vpo%5Cu003d%22%2C%22issuer%22%3A%22http%3A%2F%2Fsignin.aws.amazon.com%2Fsignin%22%2C%22signinType%22%3A%22PUBLIC%22%7D; awsc-color-theme=light; noflush_awsccs_sid=1d1d1fba661eb4e9a139616dc492a6f916f35ab9294b31cb8ea8e87df6fa79e1; last-sign-in-session=1d1d1fba661eb4e9a139616dc492a6f916f35ab9294b31cb8ea8e87df6fa79e1; aws-signer-token_ap-northeast-2=eyJrZXlWZXJzaW9uIjoielEyOG5kVnR1X1lTbXV3eVhiNURkVDR3U056bHpOenkiLCJ2YWx1ZSI6Ik9kcFkwS3NtTnk0MG1TeHd1TDVhVXRLRXNpS2dyM3pYajBUeTNOdytWU0E9IiwidmVyc2lvbiI6MX0=; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C19320%7CMCMID%7C00517512875866021013435553301658097573%7CMCAAMLH-1669776722%7C3%7CMCAAMB-1669776722%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1669179122s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; seance=%7B%22accountId%22%3A%22801422795908%22%2C%22iam%22%3Afalse%2C%22services%22%3A%5B%5D%2C%22status%22%3A%22ACTIVE%22%2C%22exp%22%3A0%7D; awsd2c-token=eyJraWQiOiIzOTM1N2I5Ny1iYWMzLTQ5MjktOTY4NS0zZmQzMDdjMjMwMzQiLCJ0eXAiOiJjb20uYXdzLmFtYXpvbi5kMmMudnMrSldUIiwiYWxnIjoiUlMyNTYifQ.eyJ2aWQiOiIyZWMyMzI1MS0wODU4LTY0MjItMWYzMC05NTI2MjRkMzBkMTciLCJpc3MiOiJodHRwczpcL1wvdnMuYXdzLmFtYXpvbi5jb20iLCJtaWQiOiIwMDUxNzUxMjg3NTg2NjAyMTAxMzQzNTU1MzMwMTY1ODA5NzU3MyIsImV4cCI6MTY2OTE3NDE2OCwiaWF0IjoxNjY5MTczNTY4fQ.CjKk8l8sFCl3PlQbuUhOpoARIsjmV8IiVgiu2nzNVFHnoobNZ0vKYCsokJDXC6m9dLuB5T57YVTB-hQZLDUSl6943ZqU1OIXsYvEgTPkRi-OGP0o3GhU_x55ttySUr8w1Shvc6mRYb2vxoopRevxOSN9CM7wZNSDNZsrLG_Fa0vHvg7MzYVpv-18RsuonU8dG6TwZzwS16HEOSHSxYDhghzRPUzUlQDhLlXjKbRyPPfMVeABsWKLGsM4MfzUPsTEgEteFNSUFUWniiLs9cx5xNMU7F6ij7R3BQcLJK9VMa6AdTE9G9uJaHHBpdtrO-4iDM9adtbczePAbQNw7Abv8Q; awsd2c-token-c=eyJraWQiOiIzOTM1N2I5Ny1iYWMzLTQ5MjktOTY4NS0zZmQzMDdjMjMwMzQiLCJ0eXAiOiJjb20uYXdzLmFtYXpvbi5kMmMudnMrSldUIiwiYWxnIjoiUlMyNTYifQ.eyJ2aWQiOiIyZWMyMzI1MS0wODU4LTY0MjItMWYzMC05NTI2MjRkMzBkMTciLCJpc3MiOiJodHRwczpcL1wvdnMuYXdzLmFtYXpvbi5jb20iLCJtaWQiOiIwMDUxNzUxMjg3NTg2NjAyMTAxMzQzNTU1MzMwMTY1ODA5NzU3MyIsImV4cCI6MTY2OTE3NDE2OCwiaWF0IjoxNjY5MTczNTY4fQ.CjKk8l8sFCl3PlQbuUhOpoARIsjmV8IiVgiu2nzNVFHnoobNZ0vKYCsokJDXC6m9dLuB5T57YVTB-hQZLDUSl6943ZqU1OIXsYvEgTPkRi-OGP0o3GhU_x55ttySUr8w1Shvc6mRYb2vxoopRevxOSN9CM7wZNSDNZsrLG_Fa0vHvg7MzYVpv-18RsuonU8dG6TwZzwS16HEOSHSxYDhghzRPUzUlQDhLlXjKbRyPPfMVeABsWKLGsM4MfzUPsTEgEteFNSUFUWniiLs9cx5xNMU7F6ij7R3BQcLJK9VMa6AdTE9G9uJaHHBpdtrO-4iDM9adtbczePAbQNw7Abv8Q; s_sq=%5B%5BB%5D%5D; noflush_awscnm=%7B%22hist%22%3A%5B%22s3%22%2C%22home%22%2C%22upc%22%2C%22lam%22%2C%22iam%22%2C%22iam-console%22%2C%22ecr%22%2C%22cfo%22%2C%22sagemaker%22%2C%22budgets%22%2C%22sso%22%2C%22serverlessrepo%22%2C%22imagebuilder%22%2C%22ag%22%2C%22cw%22%2C%22eb%22%5D%2C%22sc%22%3A%5B%5D%2C%22tm%22%3A%22tm-both%22%2C%22ea%22%3Atrue%2C%22consoleFlags%22%3A%5B%22F%22%2C%22G%22%2C%22J%22%5D%7D'}
    minio_client.fget_object(bucket_name=bucket,
                       object_name=video_name,
                       file_path=video_path,
                       request_headers=headers)
    latency, _ = video_processing(video_name, video_path)

    ret_val = {}
    ret_val['latency'] = latency
    return ret_val
# tp={
#     "endpoint": "s3.ap-east-1.amazonaws.com",
#     "access_key": "AKIA3VGEFMSCA6L6AEXA",
#     "secret_key": "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",
#     "bucket": "bucket656056549",
#     "video": "720.avi",
#     "image": "drone.png"
# }
# main(tp)