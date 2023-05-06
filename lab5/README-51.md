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


## Security and ports

The following ports have been opened:

![ports](assets/5.1/open-ports.png)

Also the following inbound rules were added for the primary (master) node:

![security-group](assets/5.1/security-group.png)

After having enabled port 22, it was possible to connect to primary instance via ssh and then another authorized_key was
added to this instance. Now we are able to connect to ssh via linux console:

![ssh](assets/5.1/ssh-conn.png)


## Hadoop

A `hadoop` user was created and then it was possible to access the workspace:

![hadoop-user](assets/5.1/hadoop-user.png)

![hadoop-workspace](assets/5.1/hadoop-workspace.png)
