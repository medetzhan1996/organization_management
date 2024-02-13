window.WIDGET_INIT_REGISTER = window.WIDGET_INIT_REGISTER || [];
function reinit_widgets($formset_form) {
    $(window.WIDGET_INIT_REGISTER).each(function (index, func) 
    {
        func($formset_form);
    });
}

function set_index_for_fields($formset_form, index) {
    $formset_form.find(':input').each(function () {
        var $field = $(this);
        if ($field.attr("id")) {
            $field.attr(
                "id",
                $field.attr("id").replace(/-__prefix__-/, 
                 "-" + index + "-")
            );
        }
        if ($field.attr("name")) {
            $field.attr(
                "name",
                $field.attr("name").replace(
                    /-__prefix__-/, "-" + index + "-"
                )
            );
        }
    });
    $formset_form.find('label').each(function () {
        var $field = $(this);
        if ($field.attr("for")) {
            $field.attr(
                "for",
                $field.attr("for").replace(
                    /-__prefix__-/, "-" + index + "-"
                )
            );
        }
    });
    $formset_form.find('div').each(function () {
        var $field = $(this);
        if ($field.attr("id")) {
            $field.attr(
                "id",
                $field.attr("id").replace(
                    /-__prefix__-/, "-" + index + "-"
                )
            );
        }
    });
}


function add_formset_fields(_this){
    var $formset = _this.closest('.formset')
    var $total_forms = $formset.find('[id$="TOTAL_FORMS"]')
    var $new_form = $formset.find('.empty-form')
    .clone(true).attr("id", null);
    $new_form.removeClass('empty-form d-none')
    .addClass('formset-form')
    var index = parseInt($total_forms.val(), 10)
    set_index_for_fields($new_form, index)
    $formset.find('.formset-forms').append($new_form)
    add_delete_button($new_form)
    $total_forms.val(parseInt($total_forms.val(), 10) + 1);
    reinit_widgets($new_form);
    return index
}

function add_delete_button($formset_form) {
    $formset_form.find('input:checkbox[id$=DELETE]')
     .each(function () {
        var $checkbox = $(this);
        var $deleteLink = $(
            '<button class="delete btn btn-sm btn-default mb-3  ml-2" data-duration=""><i class="fa fa-trash "></i></button>'
        );
        $formset_form.find('.delete-content').append($deleteLink);
        $(this).hide();
    });
}


$('.formset-form').each(function () {
    $formset_form = $(this);
    add_delete_button($formset_form);
    reinit_widgets($formset_form);
});
$(document).on('click', '.delete', function (e) {
    e.preventDefault()
    var duration = $(this).data('duration')
    var $formset = $(this).closest('.formset-form')
    var $checkbox = $formset.find('input:checkbox[id$=DELETE]')
    $checkbox.attr("checked", "checked")
    $formset.removeClass('d-flex').hide()
    if(duration){
        var duration_val = $('#id_duration').val()
        var current_duration = duration_val ? duration_val : 30
        var service_length = $("input:not(:checked):checkbox[id$=DELETE][name*='scheduleservice_set']").filter(
                function(){return $(this).val() != ''}).length
        if(service_length == 1){
            var duration = 30
        }
        else{
            var duration = parseInt(current_duration) - parseInt(duration)
        }
        $('#id_duration').val(duration)
    }

});

function good_search(index){
    var id_good = '#id_storageoperationgood_set-' + index + '-good'
    $(id_good).selectize({
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
        }
    })
}

function service_search(index){
    var id_good = '#id_scheduleservice_set-' + index + '-service'
    var id_good_delete = '#id_scheduleservice_set-' + index + '-DELETE'
    $(id_good).selectize({
        valueField: 'id',
        labelField: 'title',
        searchField: 'title',
        placeholder: 'Поиск услуги ...',
        onInitialize: function(){
           var _this = this;
           this.revertSettings.$children.each( function(){
               $.extend(_this.options[this.value], $(this).data())
           })
        },
        onChange: function(){
            var val = this.getValue()
            var obj = $(this)[0]
            obj.$input.closest('.service-content').find('.hierarchical-service-content').html('');
        },
        load: function(query, callback) {
            if (!query  || query.length < 2) return callback();
            $.ajax({
                url: '/service/system/service/search',
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
        onItemAdd: function(value) {
            var duration_val = $('#id_duration').val()
            var current_duration = duration_val ? duration_val : 0
            var data = this.options[value]
            var service = data.id
            var equipments = data.equipments
            if(equipments){
                var equipment_button = $('#schedule-form').find('.add-equipment-formset')
                $.each(equipments, function (i, equipment) {
                        var id = equipment.id
                        var title = equipment.title
                        var equipment_length = $("select[name*='scheduleequipment_set'].selectized").filter(
                        function(){return $(this).val() == id}).length
                        if(equipment_length == 0){
                            var index = add_formset_fields(equipment_button)
                            equipment_search(index, id, title)
                        }
                        
                })
            }
            var service_length = $("select[name*='scheduleservice_set'].selectized").filter(
                function(){return $(this).val() != ''}).length
            if(service_length == 0){
                var duration = parseInt(data.duration)
            }
            else{
                var duration = parseInt(current_duration) + parseInt(data.duration)
            }
            $('#id_duration').val(duration)
            $(id_good).closest('div').find('.delete').attr("data-duration", data.duration)
            $(id_good_delete).prop('checked', false)
        },
        onItemRemove: function(value) {
            var id_duration = $('#id_duration').val()
            var id_duration_val = id_duration ? id_duration : 0
            var data = this.options[value]
            var duration = parseInt(id_duration_val) - parseInt(data.duration)
            $('#id_duration').val(duration)
            var service_length = $("select[name*='scheduleservice_set'].selectized").filter(
                function(){return $(this).val() != ''}).length
            if(service_length == 0){
                $('#id_duration').val(30)
                $('#equipment-content').html('')
            }
            $(id_good_delete).prop('checked', true)
            
        }
    })
}

function equipment_search(index, val='', text=''){
    var id_equipment = '#id_scheduleequipment_set-' + index + '-equipment'
    var id_equipment_delete = '#id_scheduleequipment_set-' + index + '-DELETE'
    if(val && text){
        $(id_equipment).append($("<option>").val(val).text(text))
    }
    
    $(id_equipment).selectize({
        valueField: 'id',
        labelField: 'title',
        searchField: 'title',
        placeholder: 'Поиск ресурса ...',
        load: function(query, callback) {
            if (!query  || query.length < 2) return callback();
            $.ajax({
                url: '/equipment/system/equipment/search',
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
        onItemAdd: function(value) {
            $(id_equipment_delete).prop('checked', false)
        },
        onItemRemove: function(value) {
            $(id_equipment_delete).prop('checked', true)
        }
    })
}

$(document).on("click", ".add-service-formset, .add-equipment-formset, .add-good-formset, .add-pay-formset", function() {
    var index = add_formset_fields($(this))
    if($(this).hasClass('add-service-formset')){
        service_search(index)
        var id = '#id_scheduleservice_set-' + index + '-service-selectized'
        $(id).click()
        $(id).closest('div').addClass('focus input-active')
    }
    if($(this).hasClass('add-equipment-formset')){
        equipment_search(index)
    }
    if($(this).hasClass('add-good-formset')){
        good_search(index)
    }
})


 