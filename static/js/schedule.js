function user_event_refetch(calendar, url){
  $('#event-url').val(url)
  calendar.refetchEvents()
}

function resource_event_refetch(calendar, url){
  $('#resource-url').val(url)
  calendar.refetchResources()
}

function customer_detail(id){
  $.ajax({
    url: `/customer/detail/${id}`,
    type: 'GET',
    success: function(data) {
      $('#customer-search-content').addClass('d-none')
      $('#customer-detail-content').html(data).removeClass('d-none')
    }
  })
}

function customer_data(id){
  $.ajax({
    url: `/customer/data/${id}`,
    type: 'GET',
    success: function(data) {
      $('#customer-data-content').html(data)
    }
  })
}

function customer_selectize_set_val(id, name){
    var $select = $("#id_customer").selectize()
    var selectize = $select[0].selectize
    selectize.addOption({id: id, name: name})
    selectize.setValue(id)
}

function customer_search(){
	$('#id_customer').selectize({
		valueField: 'id',
		labelField: 'name',
		searchField: 'name',
		placeholder: 'Поиск клиента ...',
		options: [],
		load: function(query, callback) {
			if (!query  || query.length < 2) return callback();
			$.ajax({
			    url: '/customer/search/',
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
			if(value){
                customer_detail(value)
			}
		}
	})
}

function user_equipment_search(){
	$('.user_equipment').select2({
        dropdownParent: $('#schedule-modal-content'),
        width: '100%'
    }).on('select2:select', function (e) {
        var resource = $(this).find(':selected').attr('data-resource')
        if(resource == 'user'){
            $('#id_content_type').val(10).change()
        }
        else if(resource == 'equipment'){
            $('#id_content_type').val(38).change()
        }
    })
}

function validate_form(){
    $('#id_scheduleservice_set-0-service').removeClass('error-show')
    $('#id_user').removeClass('error-show')
    $('#id_date').removeClass('error-show')
    var user = $('#id_user').val()
    var service = $('#id_scheduleservice_set-0-service').val()
    var date = $('#id_date').val()
    if(!service || !user || !date){
      $(this).focusout()
      if(!service){
        $('#id_scheduleservice_set-0-service').addClass('error-show')
      }
      if(!user){
        $('#id_user').addClass('error-show')
      }
      if(!date){
        $('#id_start_event_date').addClass('error-show')
      }
      return false
    }
    return true
}

/*function display_price_duration(price, duration){
    $('#id_price').prop('value', price)
    $('#id_duration').prop('value', duration)
    $('#content-duration-price').removeClass('d-none')
}*/

// Найти ближайшее время для записи
function get_closest_time(arr, time) {
  	return arr.reduce(function(prev, curr) {
  		time = moment(time, 'HH:mm:ss')
  		curr_time = moment(curr, 'HH:mm:ss')
  		prev_time = moment(prev, 'HH:mm:ss')
  		curr_time_res = curr_time.diff(time, 'minutes')
  		prev_time_res = prev_time.diff(time, 'minutes')
    	return Math.abs(curr_time_res) < Math.abs(prev_time_res) ? curr : prev;
  	});
}

function get_free_slots(user, date, duration){
	$.ajax({
      	url: "/register/free/slots",
      	type: 'GET',
      	data: {
      		user: user,
        	date: date,
        	duration: duration
      	},
      	success: function(data) {
          var output = ''
          $.each(data.free_slots, function (index, time) {
            var time_short = moment(time, 'HH:mm:ss').format('HH:mm')
            output += '<option value="'+time+'">'+time_short+'</option>'
          })
          /*var closest_time = get_closest_time(data.free_slots, start_time)
          closest_time_short = moment(closest_time, 'HH:mm:ss').format('HH:mm')
          output += '<option value="'+closest_time+'" hidden selected>'+closest_time_short+'</option>'*/
          $('#id_start_time').html(output)
      	}
    })
}


$(document).on('click', '.customer-cancel', function(){
  $('#customer-modal-content').addClass('d-none').html('')
  $('#schedule-modal-content').removeClass('d-none')
})

$(document).on('click', '#add-customer', function(){
  $.ajax({
    type: "GET",
    url: "/customer/create/",
    success: function(data) {
      $('#schedule-modal-content').addClass('d-none')
      $('#customer-modal-content').removeClass('d-none').html(data)
    }
  })
})

$(document).on('click', '#cancel-customer', function(){
  $('#customer-detail-content').addClass('d-none')
  $('#customer-search-content').removeClass('d-none')
  $("#id_customer")[0].selectize.clear()
})

$(document).on('click', '#update-customer', function(){
  var id = $(this).data('id')
  $.ajax({
    type: "GET",
    url: `/customer/update/${id}`,
    success: function(data) {
      $('#schedule-modal-content').addClass('d-none')
      $('#customer-modal-content').removeClass('d-none').html(data)
    }
  })
})


$(document).on('submit', '#customer-form', function(e){
  e.preventDefault()
  var form = $('#customer-form')
  $.ajax({
    type: form.attr('method'),
    url: form.attr('action'),
    data: form.serialize(),
    success: function(data) {
      if(data.status){
        $('#customer-modal-content').addClass('d-none')
        $('#schedule-modal-content').removeClass('d-none')
        customer_detail(data.id)
        customer_selectize_set_val(data.id, data.name)
      }
    }
  })
})


function set_url_params(params, modify_href=true){
  var queryParams = new URLSearchParams(window.location.search)
  for(var i in params){
    queryParams.set(i, params[i])
  }        
  params_to_string = queryParams.toString()
  history.replaceState(null, null, "?"+queryParams.toString())
  if(modify_href && $('.modify-href').length){
    var modify = $('.modify-href').attr('href').split('?')[0] + '?' + queryParams.toString()
    $('.modify-href').attr('href', modify)
  }
  
}

/*function get_free_slots(free_slots=true){
  var user = $('#id_user').val()
  var date = $('#id_date').val()
  var duration = $('#id_duration').val()
  var start_time =  moment().format('HH:mm:ss')
  if(free_slots){
    get_free_slots(user, date, start_time, duration)
  }
}*/

function schedule_form(url, info=false, create=false, auth_user=false, auto_add_service=false, customer_trigger=false){
  $.ajax({
    url: url,
    type: 'GET',
    data: {
        url: url
    },
    success: function(data) {

      var date = moment().format("YYYY-MM-DD")
      $('#schedule-modal-content').html(data)
      $('#scheduleFormModal').modal('show')
      if(auto_add_service){
        $('.add-service-formset').trigger('click')
      }
      if(customer_trigger){
        $('#add-customer').trigger('click')
      }
      else{
        $('#schedule-modal-content').removeClass('d-none')
        $('#customer-modal-content').addClass('d-none')
      }

      if(info){
        var start_datetime = info.startStr
        var start_date = moment(start_datetime).format('YYYY-MM-DD')
        var start_time = moment(start_datetime).format('HH:mm:ss')
        var start_time_short = moment(start_datetime).format('HH:mm')
        var mode = $('#mode').val()
        if(create){
          if(mode == 'weekly'){
            var resource = $('#resource-val').val()
          }
          else{
            var resource = info.resource.id
          }
          $('#id_date').val(start_date)
          var resource_type = $('#resource-type').val()
          if(resource_type == 'user'){
            $("#id_object_id optgroup[data-resource='equipment']").remove()
            $("#id_object_id").val(resource)
            $('#id_content_type').val(10)
          }
          if(resource_type == 'equipment'){
            $("#id_object_id optgroup[data-resource='user']").remove()
            $("#id_object_id").val(resource)
            $('#id_content_type').val(38)
          }          
          $('#id_start_time').append('<option value="'+start_time+'" selected hidden>'+start_time_short+'</option>')
        }
      }
      else if(create){
          var duration = $('#id_duration').val()
          $('#id_user').val(auth_user)
          $('#id_date').val(date)
          get_free_slots(auth_user, date, duration)    
      }
      var scheduleservice_total = $('#id_scheduleservice_set-TOTAL_FORMS')
      scheduleservice_total.val() == 0 ? scheduleservice_total.val(1) : ''
      for (let i = 0; i < scheduleservice_total.val(); i++) {
        service_search(i)
      }
      customer_search()
      user_equipment_search()
    }
  })
}

$(document).on("click", ".fill-last-customer", function() {
    var id = $(this).data('id')
    var name = $(this).data('name')
    customer_detail(id)
    customer_data(id)
    customer_selectize_set_val(id, name)
  })

  $(document).on('submit', '#cashier-form', function(e){
    e.preventDefault()
    var form = $('#cashier-form')
    $.ajax({
          type: form.attr('method'),
          url: form.attr('action'),
          data: form.serialize(),
          success: function(response) {
            $('#scheduleFormModal').modal('hide')
            $("#myToast").toast("show").find('.toast-body').html('Данные оплаты успешно сохранены !')
          }
      });
  })

  $(document).on('blur', '[id*="id_scheduleservice_set"]', function(e){
    var sum_invoice = 0
    var paid = 0
    var index = $(this).attr('id').split('-')[1]
    var quantity = $('#' + 'id_scheduleservice_set-'+ index +'-quantity').val()
    var price = $('#' + 'id_scheduleservice_set-'+ index +'-price').val()
    var discount = $('#' + 'id_scheduleservice_set-'+ index +'-discount').val()
    var invoice = (quantity * price) - (discount/100) * price
    $(this).closest('.formset-form').find('.invoice').html(invoice)
    $(".invoice").each(function() {
        sum_invoice += parseInt($(this).html(), 10)
    })
    $('#sum-invoice').html(sum_invoice)
    $('#id_invoice').val(sum_invoice)
    /*var is_paid_edit = $('#id_customerpaidinvoice_set-0-paid').data('editer')
    if(is_paid_edit){
        $('#id_customerpaidinvoice_set-0-paid').val(sum_invoice)
    }
    $('#id_customerpaidinvoice_set-0-paid').val()*/
    $('.paid').each(function() {
        if($(this).val()){
          paid += parseInt($(this).val(), 10)
        }
    })
    $('#id_remainder').val(parseInt(sum_invoice) - parseInt(paid))
  })

  $(document).on('blur', '.paid', function(e){
    var paid = 0
    var sum_invoice = $('#sum-invoice').text()
    $('.paid').each(function() {
        if($(this).val()){
          paid += parseInt($(this).val(), 10)
        }
        
    })
    var remainder = parseInt(sum_invoice) - parseInt(paid)
    $('#id_remainder').val(remainder)
  })

  $(document).on('click', '.schedule-open', function(e){
    var url = $(this).data('url')
    schedule_form(url)
  })

 $(document).on('click', '.add-service', function(e){
    var url = $(this).data('url')
    schedule_form(url, false, false, false, true)
  })


 $(document).on('click', '.back-schedule', function(e){
    var url = $(this).data('url')
    schedule_form(url)
 })

  /*$(document).on('change', '#id_object_id', function(e){
    var resource = $(this).find(':selected').attr('data-resource')
    if(resource_type == 'user'){
        $('#id_content_type').val(10)
    }
    else if(resource_type == 'equipment'){
        $('#id_content_type').val(38)
    }
 })*/

 $(document).on('click', '#api-customer-search', function(e){
    var search_val = $('#id_iin').val();
    var url = $(this).data('url');
    $.ajax({
        type: 'get',
        url: url,
        data: {search_val: search_val},
        success: function(response) {
            // Handle the response from the first API (data1)
            const gender = response.data1.gender;
            $('#id_last_name').val(response.data1.last_name);
            $('#id_first_name').val(response.data1.first_name);
            $('#id_surname').val(response.data1.surname);
            $('#id_date_birth').val(response.data1.birthday);
            $('#id_address').val(response.data1.address);
            $('#id_place_work').val(response.data1.place_work);
            $('#id_phono_number').val(response.data1.telephone_number);

            if(gender){
                if(gender == 'Мужчина'){
                    $('#id_gender').val('man');
                }
                else{
                    $('#id_gender').val('woman');
                }
            }

            var html_data = '';

            $.each(response.data1.customer_insurance, function (index, value){
                html_data += `<div class="row">
                    <div class="col-md-12">
                        <h5>Страховая карта</h5>
                    </div>
                    <div class="col-md-12">
                        <label><b>Номер карты :</b></label>
                        ${value.card_number}
                    </div>
                    <div class="col-md-12">
                        <label><b>Программа :</b></label>
                        ${value.program}
                    </div>
                    <div class="col-md-12">
                        <label><b>Страховщик :</b></label>
                        ${value.insurance}
                    </div>
                    <div class="col-md-12">
                        <label><b>Дата начала :</b></label>
                        ${value.begin_date}
                    </div>
                    <div class="col-md-12">
                        <label><b>Дата окончания :</b></label>
                        ${value.end_date}
                    </div>
                </div>`;
            });

            $('#id_insurance_content').html(html_data);

            // Handle the response from the second API (data2)
            // This is a placeholder. Update this part based on your data2 structure and display requirements.
            // For example, if you want to update a certain DOM element with data from the second API:
            const statusDisplay = {
                'Planned': 'Запланировано',
                'Completed': 'Завершено',
                'Canceled': 'Отменен',
                // добавьте другие статусы по мере необходимости
            };
            professional_examination_content = '';
            let contract = '';
            let program = '';

            for (let item of response.data2) {
                for (let dataItem of item.Data) {
                    contract = `<b>Контракт</b>: ${dataItem.contract}`;
                    program = `<b>Программа</b>: ${dataItem.program}`;
                    $('#contract-id').html(contract);
                    $('#program-id').html(program);

                    $.each(dataItem.services, function(index, value) {
                        let humanReadableStatus = statusDisplay[value.status] || value.status;
                        professional_examination_content += `<div class="row">
                            <div class="col-md-12">
                                <h5>Обследование Назначение</h5>
                            </div>
                            <div class="col-md-12">
                                <label><b>Услуга :</b></label>
                                ${value.service_title}
                            </div>
                            <div class="col-md-12">
                                <label><b>Доктор код :</b></label>
                                ${value.doctor_code}
                            </div>
                            <div class="col-md-12">
                                <label><b>Дата :</b></label>
                                ${value.date_time}
                            </div>
                            <div class="col-md-12">
                                <label><b>Статус :</b></label>
                                ${humanReadableStatus}
                            </div>
                        </div>`;
                    });
                }
                }

            $('#id_customer_professional_examination_content').html(professional_examination_content);

            // Add more logic as required to handle and display the data from the second API.
        }
    });
});




