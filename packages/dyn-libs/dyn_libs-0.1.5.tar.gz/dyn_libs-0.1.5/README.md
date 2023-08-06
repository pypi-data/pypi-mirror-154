Example config
```
[Elastic]
index = dyn_test
doc_type = df
```

<h2>Change logs</h2>
* 0.1.5
    1) remove doc_type
* 0.1.4
    1) upgrade elasticsearch_client to 7.17.4
* 0.1.3
    1) remove some print
    2) fix create mapping integer to long
* 0.1.2
    1) fix missing model elastic
*  0.1.1
    1) add singleton to ElasticSearchBaseModel

*  0.1.0
    1) use elastic base model
    2) change function args <b>add_els_config</b>
    <pre>
    def add_els_config(self, index, doc_type):
        self.index = index
        self.doc_type = doc_type
    </pre>
