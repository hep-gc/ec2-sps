ec2-sps
=======
A service to filter aggregate EC2 spot prices  
print 'usage: python SpotPriceServiceAPI -[h rt jt jo je jp it nt r z ft df] <NAME/VALUE>'
    print "  -h   :usage"
    print("  -rt  :request type NAME needs to be one of 'current_spot_price','list_all_spot_price','periodic_spot_price'")
    print("  -jt  :spot cost search start time and ISO Date String i.e. '2014-03-02T20:09:07.157Z' ")
    print("  -jo  :spot cost search stop time and ISO Date String i.e. '2014-03-02T20:09:07.157Z' - later than or equal to job start time")
    print("  -je  :job execution time in hours i.e. '7' ")
    print("  -jp  :periodic time - in hours- i.e. '168' - is one week ")
    print("  -it  :image type needs to be one of 'Linux/UNIX','SUSE Linux','Windows' ")
    print("  -nt  :instance type needs to be one of 't1.micro','m3.medium','c3.2xlarge','m3.large','cc2.8xlarge','m1.medium' ")
    print("  -r   :region type needs to be one or more of 'us-east-1','us-west-1','us-west-2','eu-west-1','ap-northeast-1','ap-southeast-1','ap-southeast-2','sa-east-1' ")
    print("  -z   :zone type needs to be one or more of region+'a','b','c','d' i.e., 'us-west-2a','us-west-2b' ")
    print("  -ft  :filter type needs to be one of 'none','average','highest' ")
    print("  -df  :data filter needs to be one of 'json','html' ")
    print("")
    print("")
    print("Example Usage")
    print("--------------")
    print("To determine current spot price of an m3.medium vm type in region us-west-2 and return all results in json format")
    print("")
    print("blogins@machine:~$ python SpotPriceServiceClient.py -rt current_spot_price -it Linux/UNIX -nt m3.medium -r us-west-2 -ft none -df json ")
    print("")
    print("")
    print("To determine current spot price of 2 vm types in 2 regions and return the average result in html format")
    print("")
    print("blogins@machine:~$ python SpotPriceServiceClient.py -rt current_spot_price -it Linux/UNIX -nt t1.micro m1.medium -r us-west-2 us-west-1 -ft average -df html ")
    print("")
    print("")
    print("To determine periodic (over past 3 months, every Monday from 8:09pm till Tuesday 4:09am = 8 hour job) spot price of an m3.medium vm type in region us-west-2 and return all results in json format")
    print("")
    print("blogins@machine:~$ python SpotPriceServiceClient.py -rt periodic_spot_price -it Linux/UNIX -jt 2014-01-02T20:09:07.157Z -jo 2014-03-02T20:09:07.157Z -je 8 -jp 168 -nt m3.medium -r us-west-2 -ft none -df json ")
    print("")
    print("")
