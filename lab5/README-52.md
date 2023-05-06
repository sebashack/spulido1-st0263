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

## 3.1) List files

![ssh-list](assets/5.2/list-files.png)

## 3.2) Create datasets dir

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
