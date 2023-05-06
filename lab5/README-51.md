```
- ST0263, Lab 5.1
- Sebastian Pulido Gomez, spulido1@eafit.edu.co
- Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
```


# EMR Lab

## Cluster creation

A cluster has been created via the EMR creation form. First, the customized linux image was specified:

![linux-image](assets/5.1/creation-linux-image.png)

Then the capacity of the instances was set:

![instance-groups](assets/5.1/creation-instance-groups-conf.png)

Subsequently, the s3 persistence configuration and the vockey were specified:

![s3-vockey](assets/5.1/creation-vockey-and-s3.png)

Finally, roles default roles were configured:

![roles](assets/5.1/creation-roles.png)

20 minutes or so after the form is submitted, the cluster is ready to be used:

![created](assets/5.1/cluster-created.png)


## S3 bucket creation

The s3 bucket to save jupyter notebooks was created:

![s3](assets/5.1/s3bucket.png)
