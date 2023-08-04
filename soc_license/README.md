# soc-license

```shell
curl -c /tmp/soc-license-cookie -b /tmp/soc-license-cookie http://127.0.0.1/license/
curl -X POST -d '{"firstname": "Prenom", "lastname":"Nom", "lang":"fr"}' -c /tmp/soc-license-cookie -b /tmp/soc-license-cookie http://127.0.0.1/license/

curl -c /tmp/soc-license-cookie -b /tmp/soc-license-cookie http://127.0.0.1/license/
curl -X POST -d '{"question": "q_description", "answer":"a_id"}' -c /tmp/soc-license-cookie -b /tmp/soc-license-cookie http://127.0.0.1/license/
```

