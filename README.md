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

```
import valispace
```

**And initialize with:**

```
vali = valispace.API()
```

At this step you will need to enter your Valispace url (e.g. https://demo.valispace.com), username and password for authentication.

Then use the Valispace API like this:

**Get a dict of an entire data type:**

```
all_valis = vali.all_data(type='vali')
```

The type field can be: '*component*', '*vali*', '*textvali*' or '*tag*'

**Post new data:**

```
vali.post_data(type='vali', data=JSON)

```

The input data should be a single JSON object. Check the examples:
```
import valispace
valispace = valispace.API()

# -- Insert new Component --
vali.post_data(type='component', data="""{
        "name": "component_name",
        "description": "Insert description here",
        "parent": null,
        "project": 25,
        "valis": [],
        "tags": [30, 31, 32]
    }""")

# -- Insert new Vali --
vali.post_data(type='vali', data="""{
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
all_vali_names = vali.all_vali_names()
```

**Get a Vali with all properties:**

```
a = vali.get_vali(id=50)
b = vali.get_vali(name="Fan.Mass")
```

**Get the value of a Vali:**

```
value = vali.get_vali_value(id=50)
```

**Update a Vali formula:**

```
vali.update_vali(id=50, formula=str(value + 1))
```

**Get a matrix:**

```
matrix = vali.get_matrix_str(id=57)
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
