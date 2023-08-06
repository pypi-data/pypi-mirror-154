
# Minio-hung: Print your .csv file from Minio
## Powered by Ly Duc Hung (FPT Infomation System)

# How to install?
```
pip install Minio-hung
```
## or

Windows
```
py -m pip install Minio-hung
```
Linux/Mac OS
```
python3 -m pip install Minio-hung
```

# What's in package?
```
thuviencuabomay
```

# How to use Minio-hung?
## You know this package that use to print .csv Minio file. You can use to one of codes below here:

ACCESS_KEY: Access key in your Services Account.

SECRET_KEY: Secret key in your Services Account.

BUCKET_NAME: Your Bucket name.

OBJECT_NAME: The Object name in your Bucket.

```
#1
import thuviencuabomay

thuviencuabomay.Read(ACCESS_KEY, SECRET_KEY, BUCKET_NAME, OBJECT_NAME)



#2
from thuviencuabomay import Read

Read(ACCESS_KEY, SECRET_KEY, BUCKET_NAME, OBJECT_NAME)

```