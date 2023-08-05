# kuflow_rest_client.TaskApi

All URIs are relative to *https://api.kuflow.com/v1.0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**actions_append_log**](TaskApi.md#actions_append_log) | **POST** /tasks/{id}/~actions/append-log | Append a log to the task
[**actions_delete_element**](TaskApi.md#actions_delete_element) | **POST** /tasks/{id}/~actions/delete-element | Delete an element by code
[**actions_delete_value_document**](TaskApi.md#actions_delete_value_document) | **POST** /tasks/{id}/~actions/delete-element-value-document | Delete an element document value
[**actions_save_element**](TaskApi.md#actions_save_element) | **POST** /tasks/{id}/~actions/save-element | Save an element
[**actions_save_element_value_document**](TaskApi.md#actions_save_element_value_document) | **POST** /tasks/{id}/~actions/save-element-value-document | Save an element document

# **actions_append_log**
> Task actions_append_log(idlog)

Append a log to the task

A log entry is added to the task. If the number of log entries is reached, the oldest log entry is removed.

### Example

* Basic Authentication (BasicAuth):
```python
import kuflow_rest_client
from kuflow_rest_client.api import task_api
from kuflow_rest_client.model.log import Log
from kuflow_rest_client.model.task import Task
from pprint import pprint
# Defining the host is optional and defaults to https://api.kuflow.com/v1.0
# See configuration.py for a list of all supported configuration parameters.
configuration = kuflow_rest_client.Configuration(
    host = "https://api.kuflow.com/v1.0"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: BasicAuth
configuration = kuflow_rest_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)
# Enter a context with an instance of the API client
with kuflow_rest_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = task_api.TaskApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "id_example",
    }
    body = Log(
        id="id_example",
        created_at="1970-01-01T00:00:00.00Z",
        message="message_example",
        level=LogLevel("INFO"),
    )
    try:
        # Append a log to the task
        api_response = api_instance.actions_append_log(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except kuflow_rest_client.ApiException as e:
        print("Exception when calling TaskApi->actions_append_log: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

#### SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Log**](Log.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

#### IdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Log entry added

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Task**](Task.md) |  | 



[**Task**](Task.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **actions_delete_element**
> Task actions_delete_element(iddelete_element_command)

Delete an element by code

Allow to delete task element by specifying the item definition code.  Remove all the element values. 

### Example

* Basic Authentication (BasicAuth):
```python
import kuflow_rest_client
from kuflow_rest_client.api import task_api
from kuflow_rest_client.model.default_error import DefaultError
from kuflow_rest_client.model.task import Task
from kuflow_rest_client.model.delete_element_command import DeleteElementCommand
from pprint import pprint
# Defining the host is optional and defaults to https://api.kuflow.com/v1.0
# See configuration.py for a list of all supported configuration parameters.
configuration = kuflow_rest_client.Configuration(
    host = "https://api.kuflow.com/v1.0"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: BasicAuth
configuration = kuflow_rest_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)
# Enter a context with an instance of the API client
with kuflow_rest_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = task_api.TaskApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "id_example",
    }
    body = DeleteElementCommand(
        code="code_example",
    )
    try:
        # Delete an element by code
        api_response = api_instance.actions_delete_element(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except kuflow_rest_client.ApiException as e:
        print("Exception when calling TaskApi->actions_delete_element: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

#### SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeleteElementCommand**](DeleteElementCommand.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

#### IdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Task elements deleted
default | ApiResponseForDefault | Unexpected error

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Task**](Task.md) |  | 


#### ApiResponseForDefault
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor0ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor0ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DefaultError**](DefaultError.md) |  | 



[**Task**](Task.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **actions_delete_value_document**
> Task actions_delete_value_document(iddelete_element_value_document_command)

Delete an element document value

Allow to delete a specific document from an element of document type using its id.  Note: If it is a multiple item, it will only delete the specified document. If it is a single element, in addition to the document, it will also delete the element. 

### Example

* Basic Authentication (BasicAuth):
```python
import kuflow_rest_client
from kuflow_rest_client.api import task_api
from kuflow_rest_client.model.default_error import DefaultError
from kuflow_rest_client.model.delete_element_value_document_command import DeleteElementValueDocumentCommand
from kuflow_rest_client.model.task import Task
from pprint import pprint
# Defining the host is optional and defaults to https://api.kuflow.com/v1.0
# See configuration.py for a list of all supported configuration parameters.
configuration = kuflow_rest_client.Configuration(
    host = "https://api.kuflow.com/v1.0"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: BasicAuth
configuration = kuflow_rest_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)
# Enter a context with an instance of the API client
with kuflow_rest_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = task_api.TaskApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "id_example",
    }
    body = DeleteElementValueDocumentCommand(
        document_id="document_id_example",
    )
    try:
        # Delete an element document value
        api_response = api_instance.actions_delete_value_document(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except kuflow_rest_client.ApiException as e:
        print("Exception when calling TaskApi->actions_delete_value_document: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

#### SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeleteElementValueDocumentCommand**](DeleteElementValueDocumentCommand.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

#### IdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Task elements deleted
default | ApiResponseForDefault | Unexpected error

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Task**](Task.md) |  | 


#### ApiResponseForDefault
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor0ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor0ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DefaultError**](DefaultError.md) |  | 



[**Task**](Task.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **actions_save_element**
> Task actions_save_element(idtask_element_value_or_array_value)

Save an element

Allow to save an element i.e., a field, a decision, a form, a principal or document.  In the case of document type elements, this method only allows references to be made to other existing document type elements for the purpose of copying that file into the element. To do this you need to pass a reference to the document using the 'uri' attribute. In case you want to add a new document, please use the corresponding API method. If values already exist for the provided element code, it replaces them with the new ones, otherwise it creates them. The values of the previous elements that no longer exist will be deleted. To remove an element, use the appropriate API method. 

### Example

* Basic Authentication (BasicAuth):
```python
import kuflow_rest_client
from kuflow_rest_client.api import task_api
from kuflow_rest_client.model.default_error import DefaultError
from kuflow_rest_client.model.task_element_value_or_array_value import TaskElementValueOrArrayValue
from kuflow_rest_client.model.task import Task
from pprint import pprint
# Defining the host is optional and defaults to https://api.kuflow.com/v1.0
# See configuration.py for a list of all supported configuration parameters.
configuration = kuflow_rest_client.Configuration(
    host = "https://api.kuflow.com/v1.0"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: BasicAuth
configuration = kuflow_rest_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)
# Enter a context with an instance of the API client
with kuflow_rest_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = task_api.TaskApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "id_example",
    }
    body = TaskElementValueOrArrayValue(
        code="code_example",
        value=None,
    )
    try:
        # Save an element
        api_response = api_instance.actions_save_element(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except kuflow_rest_client.ApiException as e:
        print("Exception when calling TaskApi->actions_save_element: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

#### SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TaskElementValueOrArrayValue**](TaskElementValueOrArrayValue.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

#### IdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Task with element filled
default | ApiResponseForDefault | Unexpected error

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Task**](Task.md) |  | 


#### ApiResponseForDefault
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor0ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor0ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DefaultError**](DefaultError.md) |  | 



[**Task**](Task.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **actions_save_element_value_document**
> Task actions_save_element_value_document(id)

Save an element document

Allow to save an element document uploading the content.  If it is a multiple element, and the Id referenced in the body does not exist or is empty, the document will be added to the element. If the element already exists (the Id referenced in the body corresponds to an existing one), it updates it. 

### Example

* Basic Authentication (BasicAuth):
```python
import kuflow_rest_client
from kuflow_rest_client.api import task_api
from kuflow_rest_client.model.save_element_value_document_command import SaveElementValueDocumentCommand
from kuflow_rest_client.model.task import Task
from pprint import pprint
# Defining the host is optional and defaults to https://api.kuflow.com/v1.0
# See configuration.py for a list of all supported configuration parameters.
configuration = kuflow_rest_client.Configuration(
    host = "https://api.kuflow.com/v1.0"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: BasicAuth
configuration = kuflow_rest_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)
# Enter a context with an instance of the API client
with kuflow_rest_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = task_api.TaskApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "id_example",
    }
    try:
        # Save an element document
        api_response = api_instance.actions_save_element_value_document(
            path_params=path_params,
        )
        pprint(api_response)
    except kuflow_rest_client.ApiException as e:
        print("Exception when calling TaskApi->actions_save_element_value_document: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "id_example",
    }
    body = dict(
        json=SaveElementValueDocumentCommand(
            id="id_example",
            code="code_example",
            valid=True,
        ),
        file=open('/path/to/file', 'rb'),
    )
    try:
        # Save an element document
        api_response = api_instance.actions_save_element_value_document(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except kuflow_rest_client.ApiException as e:
        print("Exception when calling TaskApi->actions_save_element_value_document: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyMultipartFormData, Unset] | optional, default is unset |
path_params | RequestPathParams | |
content_type | str | optional, default is 'multipart/form-data' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

#### SchemaForRequestBodyMultipartFormData

#### Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**json** | [**SaveElementValueDocumentCommand**](SaveElementValueDocumentCommand.md) |  | 
**file** | **file_type** |  | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

#### IdSchema

Type | Description | Notes
------------- | ------------- | -------------
**str** |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | ApiResponseFor200 | Task with element filled

#### ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

#### SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Task**](Task.md) |  | 



[**Task**](Task.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

