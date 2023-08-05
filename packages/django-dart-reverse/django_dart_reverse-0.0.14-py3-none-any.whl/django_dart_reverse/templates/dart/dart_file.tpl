class RouteValue {
  String name;
  Function(Map? params) url;
  int numParams;

  RouteValue({required this.name, required this.url, required this.numParams});
}

class InvalidReverseParamsException implements  Exception {
    InvalidReverseParamsException();
  }

String? reverse(String name, [Map? params]) {
    List data = <RouteValue>[
    {% for url in urls %}
    RouteValue(
    name:'{{url.name}}',
    url:(Map? params)=> {% if url.num_params > 0 %}{% for param in url.params %}(params?['{{param}}'] != null) &&{% endfor %} true ?{% endif %} '{{url.path}}'{% if url.num_params > 0 %}: throw InvalidReverseParamsException(){% endif %},
    numParams:{{url.num_params}}),
    {% endfor %} ];
    for (RouteValue value in data) {
    if (value.name == name && value.numParams == (params?.length ?? 0)) {
    {% if not throw_exception %}
    try {
    {% endif %}
      return value.url(params);
    {% if not throw_exception %}
    }
    on InvalidReverseParamsException {
        {% if throw_warning %}
        print('Warning: Reverse parameters were named incorrectly.');
        print(params);
        {% endif %}
    }
    {% endif %}
    }
  }
  return null;
}




