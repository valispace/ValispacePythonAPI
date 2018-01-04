# Valispace Python API

The Valispace python API lets you access and update objects in your Valispace deployment.

## Getting Started

To make use of the Valispace API you must have a valid login to any Valispace deployment. If you don't have an account, you can get a demo account at [demo.valispace.com](https://demo.valispace.com). You can also find further documentation in [docs.valispace.com](http://www.valispace.com/docs/).

### Installing

Install the Valispace python API with pip:

```
pip install valispace
```

### Import the API

Import valispace API module in a python script:

```python
import valispace
```

**And initialize with:**

```python
vs = valispace.API()
```

At this step you will need to enter your Valispace url (e.g. https://demo.valispace.com), username and password for authentication, or use the one line function:

Then use the Valispace API like this:


### GET :

A dict of an entire data type:
```python
all_valis = vs.all_data(type='vali')
```
The 'type' field can be: '*component*', '*vali*', '*textvali*' or '*tag*'

**All Vali** ids and names:
```python
all_vali_names = vs.all_vali_names()
```

A **Vali** with all properties:

Argument | Example
------------- | -------------
id | `vs.get_vali(id=1)`
name | `vs.get_vali(name='Fan.Mass')`

A **matrix**:

```python
matrix = vs.get_matrix_str(id=57)
```


A **Component** with all properties:

Argument | Example
------------- | -------------
id | `vs.get_component(id=1)`
unique_name | `vs.get_component(unique_name='Blade')`


A **Project** with all properties:

Argument | Example
------------- | -------------
id | `vs.get_project(id=1)`
name | `vs.get_project(name='Fan')`

### FILTER :


List of **Valis** with the specified arguments:

Argument | Example
------------- | -------------
workspace_id | `vs.filter_vali(workspace_id=1)`
workspace_name | `vs.filter_vali(workspace_name='Default Workspace')`
project_id | `vs.filter_vali(project_id=1)`
project_name | `vs.filter_vali(project_name='Saturn_V')`
parent_id | `vs.filter_vali(parent_id=1)`
parent_name | `vs.filter_vali(parent_name='Fan')`
tag_id | `vs.filter_vali(tag_id=10)`
tag_name | `vs.filter_vali(tag_id='example_tag')`
vali_marked_as_impacted | `vs.filter_vali(vali_marked_as_impacted='10')`


List of **Components** with the specified arguments:

Argument | Example
------------- | -------------
workspace_id | `vs.filter_component(workspace_id=1)`
workspace_name | `vs.filter_component(workspace_name='Default Workspace')`
project_id | `vs.filter_component(project_id=1)`
project_name | `vs.filter_component(project_name='Fan')`
parent_id | `vs.filter_component(parent_id=1)`
parent_name | `vs.filter_component(parent_name='Fan')`
tag_id | `vs.filter_component(tag_id=10)`
tag_name | `vs.filter_component(tag_name='example_tag')`


List of **Projects** with the specified arguments:

Argument | Example
------------- | -------------
workspace_id | `vs.filter_project(workspace_id=1)`
workspace_name | `vs.filter_project(workspace_name='Default Workspace')`

### UPDATE: 
A Vali formula:
```python
vs.update_vali(id=50, formula=str(value + 1))
```

A matrix:
```python
vs.update_matrix_formulas(57, [[2.1], [0.0], [0.0]])
```


### POST
```python
vs.post_data(type='vali', data=json_object)
```

The input data should be a single JSON object. Check the examples:
```python
import valispace
vs = valispace.API()

# -- Insert new Component --
vs.post_data(type='component', data="""{
        "name": "component_name",
        "description": "Insert description here",
        "parent": null,
        "project": 25,
        "tags": [30, 31, 32]
    }""")

# -- Insert new Vali --
vs.post_data(type='vali', data="""{
        "parent": 438,
        "shortname": "mass",
        "description": "",
        "unit": "kg",
        "formula": "5",
        "minimum": null,
        "maximum": null,
        "margin_minus": "0",
        "margin_plus": "0",
        "uses_default_formula": false,
        "reference": "",
        "type": null
    }""")

# -- Insert new Textvali --
vs.post_data(type='textvali', data="""{
        "shortname": "Message",
        "text": "Message text",
        "parent": 438
    }""")

# -- Insert new Tag --
vs.post_data(type='tag', data="""{
        "name": "white-tag",
        "color": "#FFFFFF"
    }""")
```

**Notes:**
- The "name" fields should never be repeated, this will result in a error from the Valispace's REST API.
- The "valis" fields in a component are automatically updated when new valis are inserted with the component's id in the parent field

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
