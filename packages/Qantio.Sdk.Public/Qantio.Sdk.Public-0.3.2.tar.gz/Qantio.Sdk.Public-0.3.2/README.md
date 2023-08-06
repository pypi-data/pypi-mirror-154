# qantio.sdk.client

Qantio.Sdk.Client is a Python library for dealing with Qant.io time series prediction service.

## Installation

Use the package manager [pip](https://pypi.org/project/qantio.sdk.client/) to install qantio.sdk.client.

```bash
pip install qantio.sdk.client
```
## Usage

```python
import qantio.sdk.client

# Create the client with your Qant.io ApiKey
qt_client = qantio_client("ApiKey")

# Authenticate the client against the backend with your Qant.io credentials
await qt_client.Authenticate("Username", "Password")

# Create a time serie, add an measurement and send data to Qant.io backend
await qt_client.Timeseries("Id").addMeasurement("Timestamp", "MeasurementValue").Send()
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

