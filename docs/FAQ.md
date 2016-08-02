### What is network code? ###

Each network is represented by a network code. For example, Hi-net
network has a code of `0101`, while V-net `0105`. You can see the full
code list by running `python HinetContRequest.py -h`.

### What is Maxspan? And how to choose it? ###

NIED Hi-net website sets a limitation of data size in one request:

1. Record Length <= 60 min
2. Number of channels * Record Length <= 12000 min

Just take Hi-net as example, Hi-net network has about 800 station and
24000 channels. According to the limitations, the record length should
be no more than 5 minutes long in one web request. So the `Maxspan`,
allowed maximum record length, should be no more than 5 for Hi-net
network with all stations selected.

The request script `HinetContRequest.py` helps you break through the
limitation. Using this script, you can requst datas with a much longer
record length, this script will split the request into multiple
sub-requests, each has a record length no more than `Maxspan` minutes.

### What's the workflow of HinetContRequest.py? ###

1. read configure file
2. login Hi-net website
3. check whether starting time is in service period
4. if `<span>` is larger than `MaxSpan`, split this request into multiple
   sub-requests, each has a duration no larger than `MaxSpan`
5. start the first sub-request, wait until the data is ready, then
   remember the ID
6. repeat step 5 for all sub-requests, and remember all IDs
7. download all datas in zip format
8. unzip all zip files, merge all cnt files into one cnt file
9. rename and cleanup

### What's MaxSleepCount and SleepTime? ###

After posting a data request, Hi-net server will deal with this request and
prepare waveform data. During the preparation, user is not allowed to post
another new request. So user has to wait until the data is ready.

The script will check the status of data preparation. If the data is not ready,
it will sleep for `SleepTime` seconds, and then check the status again, until
the data is ready or the number of checks larger than `MaxSleepCount`.

So the maximum sleep time for one request is MaxSleepCount\*SleepTime seconds,
if the data is still not ready, the script will report an error.

