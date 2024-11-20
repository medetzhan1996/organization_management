function good_search(index=''){
	var id = '#id_good' + index
	$(id).selectize({
		valueField: 'id',
		labelField: 'title',
		searchField: 'title',
		placeholder: 'Поиск товара ...',
		options: [],
		load: function(query, callback) {
			if (!query  || query.length < 2) return callback();
			$.ajax({
			    url: '/warehouse/good/search',
			    type: 'GET',
			    data: {
			        q: query
			    },
			    error: function() {
			        callback();
			    },
			    success: function(res) {
			        return callback(res)
			    }
			})
		},
		onChange: function (value) {
		}
	})
}