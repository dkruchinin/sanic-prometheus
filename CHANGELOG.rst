Changelog
=========

Version 0.1.5 (on May 17, 2018)
-------------------------------
* Add websocket support (@SirEdwin)
* Add http_status label to request latency metric (@mmniaziqb)

Version 0.1.4 (on Aug 1, 2017)
------------------------------
Add multiprocessing support

Version 0.1.3 (May 8, 2017)
---------------------------
FIX: remove early return that kills other middlewares.

Version 0.1.2 (Apr 25, 2017)
----------------------------
Starting from 0.5.0 Sanic has http[s]:// prefix
in request.url, switch to using request.path instead.

Version 0.1.0 (Apr 4, 2017)
---------------------------
First public version of sanic-prometheus
