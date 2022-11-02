# Basic boltspy use examples

See in source documentation in repo_tools.py as well (same directory as this file).
TODO: merge the in source documentation with this code examples.


```python
import boltspy as bolts
```

All classes created with .blt collection files from  `/data` are located in  `bolts.repo.classes`.

```python
bolts.repo.classes['ibeam_hea']
```

  

Class collections located in  `repo.collections`  and can be accessed by class  id:
```python
repo.collections['profile_i']
```

  

Links between classes and collection stored in  `repo.collection_classes`.

Get all classes by collection name:

```python
repo.collection_classes.get_dsts(repo.collections['profile_i'])`
```

Get collection by class  id:

```python
repo.collection_classes.get_src(repo.classes['ibeam_hea'])
```


Class parameters description:
```python
bolts.repo.classes['ibeam_hea'].parameters.description
```

> {'b': 'flange width', 'h': 'beam height', 'l': 'beam length', 'r': 'fillet radius', 'tf': 'flange thickness', 'tw': 'web thickness', 'type': 'beam type'}

  

Access class data:

```python
bolts.repo.classes['ibeam_hea'].parameters.tables[0].data
```

>{'HEA100': [96.0, 100.0, 5.0, 8.0, 12.0], 'HEA120': [114.0, 120.0, 5.0, 8.0, 12.0], ..}


List of class columns:
```python
bolts.repo.classes['ibeam_hea'].parameters.tables[0].columns
```
> ['h', 'b', 'tw', 'tf', 'r']
