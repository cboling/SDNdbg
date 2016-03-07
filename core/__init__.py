"""
Copyright (c) 2015 - 2016.  Boling Consulting Solutions , BCSW.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


def json_decode(json_data, field, default=None, raise_exception=False):
    """
    Decode a JSON leaf, returning a default or raising an exception if not found

    :param json_data: (dict) JSON data
    :param field: (str) Field to look for
    :param default: Default value if the field is not found in the JSON data
    :param raise_exception: (boolean) True if a SyntaxError exception should be raised
                            if the field is not found.  Default = False

    :return: Found data or default
    """
    if field in json_data:
        # TODO: Insert logging here
        return json_data[field]

    if raise_exception:
        # TODO: Insert logging here
        SyntaxError("Expected field %s not found in JSON data: '%s'", field, json_data)

    # TODO: Insert logging here
    return default
