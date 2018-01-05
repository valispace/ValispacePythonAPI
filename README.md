# Valispace Python API

The Valispace python API lets you access and update objects in your Valispace deployment.

## Getting Started

To make use of the Valispace API you must have a valid login to any Valispace deployment. If you don't have an account, you can get a demo account at [demo.vali.com](https://demo.vali.com). You can also find further documentation in [docs.vali.com](http://www.vali.com/docs/).

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

```
vali = vali.API()
```

At this step you will need to enter your Valispace url (e.g. https://demo.vali.com), username and password for authentication, or use the one line function:

Then use the Valispace API like this:

### GET :

A dict of an entire data type:
```python
all_valis = vali.all_data(type='vali')
```
The 'type' field can be: '*component*', '*vali*', '*textvali*' or '*tag*'

**All Vali** ids and names:
```python
all_vali_names = vali.get_vali_names()
```

A **Vali** with all properties:

Argument | Example
------------- | -------------
id | `vali.get_vali(1)`
name | `vali.get_vali_by_name('Fan.Mass')`

A **matrix**:

```python
matrix = vali.get_matrix_str(57)
```

A **Component** with all properties:

Argument | Example
------------- | -------------
id | `vali.get_component(1)`
unique_name | `vali.get_component_by_name('Blade')`


A **Project** with all properties:

Argument | Example
------------- | -------------
id | `vali.get_project(1)`
name | `vali.get_project_by_name('Fan')`

### FILTER :

List of **Valis** with the specified arguments:

Argument | Example
------------- | -------------
workspace_id | `vali.get_vali_list(workspace_id=1)`
workspace_name | `vali.get_vali_list(workspace_name='Default Workspace')`
project_id | `vali.get_vali_list(project_id=1)`
project_name | `vali.get_vali_list(project_name='Saturn_V')`
parent_id | `vali.get_vali_list(parent_id=1)`
parent_name | `vali.get_vali_list(parent_name='Fan')`
tag_id | `vali.get_vali_list(tag_id=10)`
tag_name | `vali.get_vali_list(tag_id='example_tag')`
vali_marked_as_impacted | `vali.get_vali_list(vali_marked_as_impacted='10')`


List of **Components** with the specified arguments:

Argument | Example
------------- | -------------
workspace_id | `vali.get_component_list(workspace_id=1)`
workspace_name | `vali.get_component_list(workspace_name='Default Workspace')`
project_id | `vali.get_component_list(project_id=1)`
project_name | `vali.get_component_list(project_name='Fan')`
parent_id | `vali.get_component_list(parent_id=1)`
parent_name | `vali.get_component_list(parent_name='Fan')`
tag_id | `vali.get_component_list(tag_id=10)`
tag_name | `vali.get_component_list(tag_name='example_tag')`


List of **Projects** with the specified arguments:

Argument | Example
------------- | -------------
workspace_id | `vali.get_project_list(workspace_id=1)`
workspace_name | `vali.get_project_list(workspace_name='Default Workspace')`

### UPDATE:
A Vali formula:
```python
vali.update_vali(50, formula=str(value + 1))
```

A matrix:
```python
vali.update_matrix_formulas(57, [[2.1], [0.0], [0.0]])
```


### POST
```python
vali.post_data(type='vali', data=json_object)
```

The input data should be a single JSON object. Check the examples:
```python
import valispace
valispace = vali.API()

# -- Insert new Component --
vali.post_data(type='component', data="""{
        "name": "component_name",
        "description": "Insert description here",
        "parent": null,
        "project": 25,
        "tags": [30, 31, 32]
    }""")

# -- Insert new Vali --
vali.post_data(type='vali', data="""{
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
vali.post_data(type='textvali', data="""{
        "shortname": "Message",
        "text": "Message text",
        "parent": 438
    }""")

# -- Insert new Tag --
vali.post_data(type='tag', data="""{
        "name": "white-tag",
        "color": "#FFFFFF"
    }""")
```
**Notes:**
- The "name" fields should never be repeated, this will result in a error in the REST API.
- The "valis" are automatically updated when new valis with this componenet id are inserted

**Get all Vali ids and names:**
```
all_vali_names = vali.get_vali_names()
```

**Get a Vali with all properties:**

```
a = vali.get_vali(50)
b = vali.get_vali_by_name("Fan.Mass")
```

**Get the value of a Vali:**

```
value = vali.get_vali_value(50)
```

**Update a Vali formula:**

```
vali.update_vali(50, formula=str(value + 1))
```

**Get a matrix:**

```
matrix = vali.get_matrix_str(57)
```

**Update a matrix:**

```
vali.update_matrix_formulas(57, [[2.1], [0.0], [0.0]])
```

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
