*mywebpy is a fork from webpy / webpy*

Add following features:

1. Use the custom wsgiserver to instead of cheroot.

2. add a function:communicateWithConn to process continued post in one session


If you want to use web.py.web.py is a web framework for Python that is as simple as it is powerful.

Visit http://webpy.org/ for more information.


The latest stable release only supports Python >= 3.5.
To install it, please run:
```
# For Python 3
python3 -m pip install mywebpy
```

Install it manually:
```
cd webpy/
python3 setup.py install
```

How to use communicateWithConn?:

```python
import web
environ = web.ctx.environ
conn = environ['SERVER_CONN']
req = environ['SERVER_REQ']
message = '<http response data>'
result_data,result_req = conn.communicateWithConn(req,message,60)
```

