# opsPyKit
Python toolkits for routine ops work.

## Usage

> This Kit includes useful python scripts for ops routine work.

It's master project for each submodules, you need add `--recursive` to checkout all of them:
```
git clone --recursive https://github.com/thimoonxy/opsPyKit.git
git submodule update --init --recursive
```


### ASN checking

```
C:\Users\simon>asn.py 8.8.8.8
Queried 8.8.8.8:

AS      | IP               | AS Name
15169   | 8.8.8.8          | GOOGLE - Google Inc., US
```

> It's simply querying [cymru.com](v4.whois.cymru.com)

### My pub IP checking
> Just run the script directly, it'll check your outbond put ip and shows location, ISP, pub IP info in the output

### GeoIP tool
> The ip_location.py basically has 2x ways to run:

```
$ ip_location.py
NOTE:
1. single ip as argv:
        ip_location.py 8.8.8.8
2. stdin a list of IPs with -s parm:
        cat list| ip_location.py -s
```

**Limitation**
When querying in batch with -s,
The system will automatically ban any IP addresses doing over 150 requests per minute. To unban your IP go to [ip-api](http://outgoing.ip-api.com/docs/api:batch).


### TCP port check
This is simply a alternative way for telnet command.
It shows the IP queried and the result of accessibility.
```
C:\Users\simon>portest.py www.google.com:25
216.58.197.100
failed

C:\Users\simon>portest.py www.baidu.com:443
119.75.217.109
ok
```