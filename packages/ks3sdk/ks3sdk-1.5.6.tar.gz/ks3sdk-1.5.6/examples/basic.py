# -*- coding: utf-8 -*-
import urllib.parse

from ks3.objectTagging import Tag
from ks3.xmlParsers.bucketCors import BucketCors, CORSRule
from ks3.xmlParsers.bucketCrossReplicate import BucketCrossReplicate
from ks3.xmlParsers.bucketLifecycle import BucketLifecycle, Rule as LifecycleRule, Filter as LifecycleFilter, \
  Expiration as LifecycleExpiration, Transition as LifecycleTransition
from ks3.connection import Connection, OrdinaryCallingFormat
from ks3.key import Key
from ks3.exception import S3ResponseError
import requests
import os
from datetime import datetime
import time
from ks3.xmlParsers.bucketLogging import BucketLogging

# 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
# 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。
from ks3.xmlParsers.bucketMirror import BucketMirror, AsyncMirrorRule, SyncMirrorRules, MirrorRequestSetting, HeaderSetting

ak = os.getenv('KS3_TEST_ACCESS_KEY_ID', '<YOUR_ACCESS_KEY>')
sk = os.getenv('KS3_TEST_ACCESS_KEY_SECRET', '<YOUR_SECRET_KEY>')
bucket_name = os.getenv('KS3_TEST_BUCKET', '<KS3_TEST_BUCKET>')
endpoint = 'ks3-cn-shanghai.ksyuncs.com' #os.getenv('KS3_TEST_ENDPOINT', 'ks3-cn-shanghai-internal.ksyuncs.com')

conn = Connection(ak, sk, host=endpoint, is_secure=False, ua_addon='test-ua/1') #port=8091,
key_name = 'test_key'


def getAllBuckets(project_ids=None):
  buckets = conn.get_all_buckets(project_ids=project_ids) #
  for b in buckets:
    print(b.name)

def headBucket(bucket_name):
  # 如果正常返回，则Bucket存在；如果抛出S3ResponseError
  headers = conn.head_bucket(bucket_name)
  print(headers)

def getBucketLocation(bucket_name):
  print(conn.get_bucket_location(bucket_name))

def createBucket(bucket_name):
  conn.create_bucket(bucket_name, policy='private', project_id=105150, headers={"x-kss-bucket-type": "ARCHIVE"})

def deleteBucket(bucket_name):
  try:
    conn.delete_bucket(bucket_name)
  except S3ResponseError as error:
    print('error')
    print(error)

def getBucketAcl(bucket_name):
  b = conn.get_bucket(bucket_name)
  policy = b.get_acl()
  # print(policy)
  for grant in policy.acl.grants:
    print(grant.permission, grant.display_name, grant.email_address, grant.id)

def setBucketAcl(bucket_name):
  b = conn.get_bucket(bucket_name)
  b.set_acl("private")

def manageBucketPolicy(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  bucket.set_bucket_policy(
    policy='{"Statement":[{"Resource":["krn:ksc:ks3:::jiangran123","krn:ksc:ks3:::jiangran123/*"],"Principal":{"KSC":["krn:ksc:iam::32432423:root"]},"Action":["ks3:*"],"Effect":"Allow"}]}')
  # policy = bucket.get_bucket_policy()
  # bucket.delete_bucket_policy()

def manageBucketReplication(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  try:
    print(bucket.get_bucket_crr().to_xml())
  except:
    bucket.set_bucket_crr('test-bucket-project', deleteMarkerStatus='Disabled', prefix_list=['hello'])

def getBucketLifeCycle(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  lifecycle = bucket.get_bucket_lifecycle()
  print(lifecycle.to_xml())

def setBucketLifeCycle(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  lifecycle = BucketLifecycle()
  # id 和 status 必须
  rule = LifecycleRule(id='rule1', status='Enabled')
  date = datetime(2021, 12, 12).isoformat(timespec='seconds') + '+08:00'
  rule.expiration = LifecycleExpiration(date=date)
  lifecycle.rule = [rule]
  bucket.set_bucket_lifecycle(lifecycle)


def setBucketLifeCycle2(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  # 设置object距其最后修改时间3天后过期。
  rule1 = LifecycleRule('rule1', LifecycleFilter('prefix1'),
                        status='Enabled',
                        expiration=LifecycleExpiration(days=3))

  # 设置object过期规则，指定日期之前创建的文件过期。
  rule2 = LifecycleRule('rule2', LifecycleFilter('prefix2'),
                        status='Enabled',
                        expiration=LifecycleExpiration(
                          date=datetime(2021, 12, 12).isoformat(timespec='seconds') + '+08:00'))

  # 设置存储类型转换规则，指定Object在其最后修改时间20天之后转为低频访问类型，在其最后修改时间30天之后转为归档类型。
  rule3 = LifecycleRule('rule3', LifecycleFilter('prefix3'),
                        status='Enabled',
                        transitions=[LifecycleTransition(days=20, storage_class='STANDARD_IA'),
                                     LifecycleTransition(days=60, storage_class='ARCHIVE')])

  # 设置存储类型转换规则，指定在指定日期之前创建的Object转为低频访问类型。
  rule4 = LifecycleRule('rule4', LifecycleFilter('prefix4'),
                        status='Enabled',
                        transitions=[
                          LifecycleTransition(date=datetime(2021, 12, 12).isoformat(timespec='seconds') + '+08:00',
                                              storage_class='STANDARD_IA')])

  print(rule1.to_xml())
  print(rule2.to_xml())
  print(rule3.to_xml())
  print(rule4.to_xml())
  lifecycle = BucketLifecycle([rule1, rule2, rule3, rule4]);
  bucket.set_bucket_lifecycle(lifecycle)

def deleteBucketLifeCycle(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  bucket.delete_bucket_lifecycle()

def getBucketLogging(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  print(bucket.get_bucket_logging().to_xml())

def setBucketLogging(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  blogging = BucketLogging(target=bucket_name, target_prefix='test_log')
  print(bucket.set_bucket_logging(blogging.to_xml()))

def enableBucketLogging(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  print(bucket.enable_logging(bucket, target_prefix='hehehehe'))

def disableBucketLogging(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  print(bucket.disable_logging())

def getBucketCors(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  print(bucket.get_bucket_cors().to_xml())

def putBucketCors(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  cors = BucketCors([CORSRule(origins=["http://dev.ksyun.com"], methods=["GET", "HEAD"], max_age="200", headers=["content-type"], exposed_headers=["content-type", "x-kss-acl"])])
  print('cors: ', cors.to_xml())
  print(bucket.set_bucket_cors(cors))

def deleteBucketCors(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  print(bucket.delete_bucket_cors())

def getBucketCrr(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  print(bucket.get_bucket_crr().to_xml())

def setBucketCrr(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  # deleteMarkerStatus 的值为 Enabled 和 Disabled
  print(bucket.set_bucket_crr('test-bucket-repli', deleteMarkerStatus="Enabled", prefix=['hello']))

def deleteBucketCrr(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  print(bucket.delete_bucket_crr())

def getBucketLogging(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  print(bucket.get_bucket_logging().to_xml())

def setBucketLogging(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  blogging = BucketLogging(target=bucket_name, target_prefix='test_log')
  print(bucket.set_bucket_logging(blogging.to_xml()))

def getBucketMirror(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  print(bucket.get_bucket_mirror())

def setBucketMirror(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  set_headers = [{
      "key": "d",
      "value": "b"
  }]
  remove_headers = [{
      "key": "d"
  }]
  pass_headers = [{
      "key": "abc"
  }]
  header_setting = HeaderSetting(set_headers=set_headers, remove_headers=remove_headers, pass_all=False, pass_headers=pass_headers)
  mirror_request_setting = MirrorRequestSetting(pass_query_string=False, follow3xx=False, header_setting=header_setting)
  async_mirror_rule = AsyncMirrorRule.rule_with_acl(mirror_urls=["http://abc.om", "http://www.wps.cn"], saving_setting_acl="private")
  sync_mirror_rules = SyncMirrorRules.rules_with_prefix_acl(key_prefixes=["abc"], mirror_url="http://v-ks-a-i.originalvod.com", mirror_request_setting=mirror_request_setting, saving_setting_acl="private")
  mirror = BucketMirror(use_default_robots=False, async_mirror_rule=async_mirror_rule, sync_mirror_rules=[sync_mirror_rules])
  print(bucket.set_bucket_mirror(mirror))

def deleteBucketMirror(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  print(bucket.delete_bucket_mirror())

#####################  ks3.billing  ###########################
from ks3.billing import get_buckets_data

def getBucketsData(bucket_names=None):
  data = get_buckets_data(ak, sk, start_time="202111192300", end_time="202111192359", bucket_names=bucket_names, products="DataSize,RequestsGet")
  print(data)

#####################  ks3.object  ###########################
def getObjectMeta(bucket_name, object_key_name):
  bucket = conn.get_bucket(bucket_name)
  k = bucket.get_key(object_key_name)
  if k:
    print(k.name, k.size, k.last_modified, k.object_type, k.tagging_count)

def uploadObjectFromFile():
  bucket = conn.get_bucket(bucket_name)
  k = bucket.new_key('big_photo')
  ret = k.set_contents_from_filename('./hsm.pdf')
  if ret and ret.status == 200:
    print("上传成功")

def uploadObjectFromString():
  bucket = conn.get_bucket(bucket_name)
  k = bucket.new_key('hello')
  # # key 和 value 需要 url 编码
  # taggingStr = 'name=jh'
  # headers = {'x-kss-tagging': taggingStr}
  ret = k.set_contents_from_string('hellodada')
  # # 请求ID。请求ID是本次请求的唯一标识，强烈建议在程序日志中添加此参数。
  # print(ret.headers['x-kss-request-id'])
  # # ETag是put_object方法返回值特有的属性，用于标识一个Object的内容。
  # print(ret.headers)
  # HTTP返回码。
  if ret and ret.status == 200:
    print("上传成功")

def downloadObjectAndPrint():
  bucket = conn.get_bucket(bucket_name)
  k = bucket.get_key('article.en.txt')
  s = k.get_contents_as_string().decode()
  print(s)

def downloadObjectAsStreamAndPrint():
  bucket = conn.get_bucket(bucket_name)
  k = bucket.get_key('shake.txt')
  bytes = k.read(300)
  print('start: ', datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
  while bytes:
    s = bytes.decode()
    print('bytes decoded:', s)
    time.sleep(5)
    bytes = k.read(300)
  print('end: ', datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))

def downloadObjectAndSave():
  bucket = conn.get_bucket('yh-test')
  k = bucket.get_key('/test/u=256227122,2429609367&fm=26&gp=0.jpg')
  k.get_contents_to_filename('article.txt')

def deleteObject(key_name):
  bucket = conn.get_bucket(bucket_name)
  try:
    bucket.delete_key(key_name)
    print("删除成功")
  except Exception as e:
    print("删除失败")
    print(e)
    pass

def getObjectAcl():
  bucket = conn.get_bucket(bucket_name)
  policy = bucket.get_acl('article.txt')
  print(policy.to_xml())

def setObjectAcl():
  bucket = conn.get_bucket(bucket_name)
  # object policy : private | public-read | public-read-write
  bucket.set_acl("public-read", '<YOUR_KEY_NAME>')

def setObjectMeta():
  b = conn.get_bucket(bucket_name)
  b.copy_key('<yourKeyName>', '<yourBucketName>', '<yourKeyName>',
             headers={'content-type': 'text/plain', 'x-kss-metadata-directive': 'REPLACE'})

def setObjectStorageClass():
  b = conn.get_bucket(bucket_name)
  b.copy_key('<yourKeyName>', '<yourBucketName>', '<yourKeyName>', headers={'x-kss-storage-class': 'STANDARD_IA'})

def copy(dstKey, srcKey):
  bucket_name = 'yh-test'
  b = conn.get_bucket(bucket_name)
  b.copy_key(dstKey, bucket_name, srcKey)

def listObjects():
  bucket = conn.get_bucket('liubo-test')
  keys = bucket.list()
  for k in keys:
    print('object:', k.name)

def listObjectsMore(bucket_name):
  bucket = conn.get_bucket(bucket_name)
  keys = bucket.list(delimiter='/', prefix='test/')
  for k in keys:
    print('object:', k.name)

def listAndDelete():
  bucket = conn.get_bucket(bucket_name)
  keys = bucket.list(delimiter='/', max_keys=10, prefix='15')
  print(keys.marker)
  for k in keys:
    print('object:', k.name)
    deleteObject(k.name)

def listObjectsAndFilter(endTime=None):
  bucket = conn.get_bucket('test-bucket')
  keys = bucket.listObjects(delimiter='/') # start_time=1640331446, end_time=1641895096
  for k in keys:
    print(k)

def getObjectTagging():
  bucket = conn.get_bucket(bucket_name)
  key = bucket.get_key('hehe')
  tagging = key.get_object_tagging()
  print(tagging.to_xml())

def setObjectTagging():
  bucket = conn.get_bucket(bucket_name)
  key = bucket.get_key('hehe')
  tagging = [Tag('name', 'jh')]
  key.set_object_tagging(tagging)

def deleteObjectTagging():
  bucket = conn.get_bucket(bucket_name)
  key = bucket.get_key('hehe')
  key.delete_object_tagging()

def calcFolderSize(bucket, folder):
  length = 0
  keys = bucket.list(prefix=folder)
  for k in keys:
    if isinstance(k, Key):
      length += k.size
  return length

from ks3.prefix import Prefix

# 列举指定目录下的文件大小
def getFolderSizeInBucket():
  bucket = conn.get_bucket(bucket_name)
  keys = bucket.list(delimiter='/')
  for k in keys:
    if isinstance(k, Prefix):
      print('dir: ' + k.name + '  size:' + str(calcFolderSize(bucket, k.name)) + "Byte")


def test_multipart_upload():
  import math, os
  from filechunkio import FileChunkIO
  bucket = conn.get_bucket(bucket_name)

  source_path = '/Users/jabbar/Codes/storage/ks3-python-sdk/examples/DSC03381.JPG'
  # 源文件大小
  source_size = os.stat(source_path).st_size

  mp = bucket.initiate_multipart_upload("big_photo.jpg", policy="public-read-write")
  print(mp)

  # chunk_size = 5242880
  chunk_size = 5242880
  chunk_count = int(math.ceil(source_size * 1.0 / chunk_size * 1.0))

  # 通过 FileChunkIO 将文件分片
  for i in range(chunk_count):
    offset = chunk_size * i
    bytes = min(chunk_size, source_size - offset)
    with FileChunkIO(source_path, 'r', offset=offset, bytes=bytes) as fp:
      # 逐个上传分片
      mp.upload_part_from_file(fp, part_num=i + 1)
  # 发送请求，合并分片，完成分片上传
  ret = mp.complete_upload()
  if ret and ret.status == 200:
    print("上传成功")

def test_fetch_object():
  bucket = conn.get_bucket(bucket_name)
  key = bucket.new_key('www-logo')
  key.fetch_object(source_url='http://fe.ksyun.com/project/resource/img/www-logo.png',
                      headers={'x-kss-acl': 'public-read'})
  print('fetch成功')

def test_generate_url(key_name, image_attrs=None):
  b = conn.get_bucket(bucket_name)
  k = b.get_key(key_name)
  if k:
    url = k.generate_url(600, image_attrs=image_attrs)  # 60s 后该链接过期
    print(url)
  else:
    print('object not found')

def test_get_presigned_url(key_name):
  b = conn.get_bucket(bucket_name)
  # 新建对象key
  k = b.new_key(key_name)
  if k:
    url = k.get_presigned_url(6000)  # 60s 后该链接过期
    print(url)
    return url

def restoreObject(key_name):
  b = conn.get_bucket(bucket_name)
  k = b.get_key(key_name)
  k.restore_object()

def test_put_via_presigned_url(key):
  url = test_get_presigned_url(key)
  with open('./article.txt', 'rb') as fp:
    result = requests.put(url, data=fp)
    print(result)
from ks3.sts import assumeRole
def test_assumeRole():
  print(assumeRole(ak, sk, "krn:ksc:iam::xxx:role/xx-test-bucket", "ks3", 3600))


# getAllBuckets(project_ids="103406")
# headBucket('test-bucket')
# getBucketLocation('hanjing-test000')
# createBucket('test-bucket-project')
# deleteBucket('test-bucket')
# getBucketAcl('test-bucket')
# setBucketAcl('test-bucket')
# manageBucketReplication('test-bucket')
# getBucketLifeCycle(bucket_name)
# setBucketLifeCycle(bucket_name)
# setBucketLifeCycle2(bucket_name)
# deleteBucketLifeCycle(bucket_name)
# getBucketLogging(bucket_name)
# setBucketLogging(bucket_name)
# disableBucketLogging(bucket_name)
# enableBucketLogging(bucket_name)
# putBucketCors(bucket_name)
# getBucketCors(bucket_name)
# deleteBucketCors(bucket_name)
# deleteBucketCrr(bucket_name)
# getBucketCrr(bucket_name)
# setBucketCrr(bucket_name)
# setBucketMirror(bucket_name)
# deleteBucketMirror(bucket_name)
# getBucketMirror(bucket_name)
##### object #####
# getObjectMeta('liubo-test', 'temp/drop-upload.gif')
# listObjects()
# listObjectsMore("liubo-test")
# listObjectsAndFilter()
# setObjectTagging()
# getObjectTagging()
# deleteObjectTagging()
# getFolderSizeInBucket();
# downloadObjectAndPrint()
# downloadObjectAsStreamAndPrint()
# downloadObjectAndSave()
# count = 20
# while True:
# uploadObjectFromFile()
#   time.sleep(5)
#   count = count - 1
# uploadObjectFromString()
# deleteObject("tellmewhy")
getObjectAcl()
# test_multipart_upload()
# test_fetch_object()
# test_generate_url('genji&ash.pn', image_attrs='@base@tag=imgScale&w=500')
# test_get_presigned_url('rds-test')
# test_put_via_presigned_url('index.html')
# listObjectsMore()
# deleteObject()
# listObjectsAndFilter()
# listAndDelete()
# restoreObject("www-logo")
# getBucketsData("test-bucket")
# test_assumeRole()

# copy('/test/u=256227122,2429609367&fm=26&gp=.jpg', 'download.png')

# fileName = "\u006b\u0073\u005f\u0073\u0063\u0061\u006e\u005f\u006f\u0063\u0072\u002f\u0032\u0030\u0031\u0038\u002d\u0030\u0033\u002d\u0031\u0032\u002f\u0010\ufffd\u0070\ufffd\ufffd\ufffd\u0002\u002e\u0057\u007f\u005b\ufffd\u0008\ufffd\u002a\ufffd\u002e\u006a\u0070\u0067";
# hehe = "�p���.W[�*�.jpg"
# for c in hehe:
#     print(repr(c), c)
# urlcoded = urllib.parse.quote(fileName)
# unquoted = urllib.parse.unquote('%FF')
# quoted = urllib.parse.quote(unquoted)
# print(unquoted)
# print(quoted)
