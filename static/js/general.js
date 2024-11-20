function set_params_url(params){
	var queryParams = new URLSearchParams(window.location.search)
	for (var key in params) {
	    param = params[key]
	    param_id = '#id_' + param
	    param_val = $(param_id).val()
	    queryParams.set(param, param_val)
	}
	history.replaceState(null, null, "?"+queryParams.toString())
	location.reload()
}