```
- ST0263, Lab 5.2
- Sebastian Pulido Gomez, spulido1@eafit.edu.co
- Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
```

# HDFS

## 1) Cluster creation

The cluster documentation was already documented [here](README-51.md).

## 2) SSH connection to master node

![ssh](assets/5.2/ssh-connection.png)

## 3) File management via terminal SSH

### 3.1) List files

![ssh-list](assets/5.2/list-files.png)

### 3.2) Create datasets dir

After running `hdfs dfs -mkdir /user/hadoop/datasets` we can list our newly created dir:

![datasets](assets/5.2/datasets-ls.png)



We have a local copy of the `datasets` dir

![datasets-local](assets/5.2/local-datasets.png)

Now we will copy that dir to `hdfs`:


![hdfs-dirs](assets/5.2/copied-dirs.png)


Now we can see that our files are visible on HUE:

![hue-gui](assets/5.2/hue-gui2.png)


## 4) File management via terminal gui

Create another dir:

![create-gui](assets/5.2/create-dir-hue.png)

Select file to upload:

![create-gui](assets/5.2/select_files.png)

See file:

![uploaded-gui](assets/5.2/file-uploaded.png)


## 5) Copy dir to S3

`spulido1-st0263]$ hadoop distcp  datasets  s3://st0263spulido/datasets/` was executed:

![copy-s3](assets/5.2/cp-to-s3.png)


`datasets` was uploaded to S3:

![s3-dir](assets/5.2/s3-files.png)


## 6) Additional comments

### 6.1) New S3 bucket

The tutorial was developed with the bucket `s3://st0263spulido`, but in order to comply with the course requirements
a bucket `s3://st0263spulido1` has been created and the contents of the previous one copied:

![s3-new](assets/5.2/new-bucket.png)


### 6.2) Solve issues with Hue not being able to connect to HDFS

This is the list of our ERM apps:

![erm-apps](assets/5.2/erm-apps.png)

Notice that HDFS is running on port 9870

However, when trying to access the HDFS file-system via HUE, we get the following error:

![hue-error](assets/5.2/hue-error.png)

The problem here is that by default HUE is configured to send requests to HDFS on port 14000, but it is running on port 9870.
The issue can be solved by editing the file `/etc/hue/conf.empty/hue.ini` via an ssh connection to the primary instance:

![hue-init](assets/5.2/hue-init.png)

The port `14000` on the image above has to be replaced with `9870` and then the hue service must be restarted with `restart hue.service`.
Also we must make sure that the port `9870` has been opened in the security groups and that public access has been enabled for it.

After these changes are applied, we should be able to see the file system:

![file-sys](assets/5.2/file-sys.png)
