# Valispace Python API

The Valispace python API lets you access and update objects in your Valispace deployment.

## Getting Started

To make use of the Valispace API you must have a valid login to any Valispace deployment. If you don't have an account, you can get a demo account at [demo.valispace.com](https://demo.valispace.com). You can also find further documentation in [docs.valispace.com](http://www.valispace.com/docs/).

### Installing

Install the Valispace python API with pip:

```
pip install valispace
```

### Using the API

**Import valispace API:**

```python
import valispace
```

**And initialize with:**

```python
valispace = valispace.API()
```

At this step you will need to enter your Valispace url (e.g. https://demo.valispace.com), username and password for authentication.

Then use the Valispace API like this:

**Get a dict of an entire data type:**

```python
all_valis = valispace.all_data(type='vali')
```
The type field can be: '*component*', '*vali*', '*textvali*' or '*tag*'

**Post new data:**

```python
valispace.post_data(type='vali', data=json_object)
```

The input data should be a single JSON object. Check the examples:
```python
import valispace
valispace = valispace.API()

# -- Insert new Component --
valispace.post_data(type='component', data="""{
        "name": "component_name",
        "description": "Insert description here",
        "parent": null,
        "project": 25,
        "valis": [],
        "tags": [30, 31, 32]
    }""")

# -- Insert new Vali --
valispace.post_data(type='vali', data="""{
        "parent": 438,
        "shortname": "mass",
        "description": "",
        "unit": "kg",
        "formula": "5",
        "wc_minus": "5",
        "wc_plus": "5",
        "minimum": null,
        "maximum": null,
        "margin_minus": "0",
        "margin_plus": "0",
        "tags": [],
        "uses_default_formula": false,
        "valis_used": [],
        "reference": "",
        "type": null
    }""")

# -- Insert new Textvali --
valispace.post_data(type='textvali', data="""{
        "shortname": "Message",
        "text": "Message text",
        "parent": 438
    }""")

# -- Insert new Tag --
valispace.post_data(type='tag', data="""{
        "name": "white-tag",
        "color": "#FFFFFF"
    }""")
```
**Notes:**
- The "name" fields should never be repeated, this will result in a error in the REST API.
- The "valis" fields in component are automatically updated when new valis with are inserted with this component id in the parent field


**Get Valis with the specified arguments:**

Argument | Example
------------- | -------------
id | `valispace.get_vali(id=1)`
name | `valispace.get_vali(name='Fan.Mass')`
workspace_id | `valispace.get_vali(workspace_id=1)`
project_id | `valispace.get_vali(project_id=1)`
parent_id | `valispace.get_vali(parent_id=1)`
parent_name | `valispace.get_vali(parent_name='Fan')`
tag_id | `valispace.get_vali(tag_id=10)`
tag_name | `valispace.get_vali(workspace_id='example_tag')`
valis_marked_as_impacted | `valispace.get_vali(valis_marked_as_impacted='10')`

**Get all Vali ids and names:**
```python
all_vali_names = valispace.all_vali_names()
```

**Update a Vali formula:**

```python
valispace.update_vali(id=50, formula=str(value + 1))
```

**Get a matrix:**

```python
matrix = valispace.get_matrix_str(id=57)
```

**Update a matrix:**

```python
valispace.update_matrix_formulas(57, [[2.1], [0.0], [0.0]])
```

**Get Components with the specified arguments:**

Argument | Example
------------- | -------------
id | `valispace.get_component(id=1)`
name | `valispace.get_component(name='Blade')`
workspace_id | `valispace.get_component(workspace_id=1)`
project_id | `valispace.get_component(project_id=1)`
project_name | `valispace.get_component(project_name='Fan')`
parent_id | `valispace.get_component(parent_id=1)`
tag_id | `valispace.get_component(tag_id=10)`
tag_name | `valispace.get_component(workspace_id='example_tag')`


**Get Projects with the specified arguments:**

Argument | Example
------------- | -------------
id | `valispace.get_project(id=1)`
name | `valispace.get_project(name='Fan')`
workspace_id | `valispace.get_project(workspace_id=1)`

<!-- ## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us. -->

## Authors

* **Valispace**

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

<!-- ## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc -->
