# Valispace Python API

The Valispace python API lets you access and update objects in your Valispace deployment.

## Getting Started

To make use of the Valispace API you must have a valid login to any Valispace deployment. If you don't have an account, you can get a demo account at [demo.valispace.com](https://demo.valispace.com). You can also find further documentation in [docs.valispace.com](http://www.valispace.com/docs/)

### Installing

Install the Valispace python API with pip:

```
pip install valispace
```

### Using the API

Import valispace API:

```
import valispace
```

And initialize with:

```
valispace = valispace.API()
```

At this step you will need to enter your Valispace url (e.g. https://demo.valispace.com), username and password for authentication.

Then use the Valispace API like this:

Get a dict of an entire data type:

```
all_valis = valispace.all_data(type='vali')
```

The type field can be a 'component', 'vali', 'textvali' or 'tag'

Post new data:

```
all_valis = valispace.post_data(type='vali')
```

Get all Vali ids and names:

```
all_vali_names = valispace.all_vali_names()
```

Get a Vali with all properties:

```
a = valispace.get_vali(id=50)
b = valispace.get_vali(name="Fan.Mass")
```

Get the value of a Vali:

```
value = valispace.get_value(id=50)
```

Update a Vali formula:

```
valispace.update_vali(id=50, formula=str(value + 1))
```

Get a matrix:

```
matrix = valispace.get_matrix_str(id=57)
```

Update a matrix:

```
valispace.update_matrix_formulas(57, [[2.1], [0.0], [0.0]])
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
