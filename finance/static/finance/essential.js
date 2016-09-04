$(document).ready( function() {

  // Make dropdowns look pretty. (Necessary for Semantic-UI).
  $('.ui.dropdown').dropdown({
    allowAdditions: true
  });

  // When a table row is clicked, redirect to a page that will populate the form with the
  // clicked entry's data and will allow editing of the entry.
  $('table tbody tr').dblclick( function() {
    var id = $(this).attr('id').split('-')[1];
    window.document.location = 'http://127.0.0.1:8000/finance/edit/' + id;
  });

  // After a row has been edited (or not) and focused out, submit the current values
  // displayed in the table to the server via ajax, the server saves the new values.
  $('#data-table tbody tr').focusout( function() {
    var entry_id = $(this).attr('data-transaction-id');
    update_row($(this), {
      id:           entry_id,
      date:         $('#date-' + entry_id).text(),
      total:        $('#total-' + entry_id).text(),
      description:  $('#description-' + entry_id).text()
    });
  });


  $('#reset-transaction').click( function() {
    clear_transaction_form();
  });


  $('#sumbmit_form_ajax').click( function() {
    $.ajax({
      url:      'http://127.0.0.1:8000/finance/submittransactionform/',
      type:     'POST',
      data:     {request_data: JSON.stringify(gather_transaction_form())},
      success:  function(response) {
                  console.log('ajax form submission successful');
                },
      error:    function (xhr,errmsg,err) {
                  console.log('failure');
                }
    });
  });


});





// The ajax request to save the current values of the transaction's row.
function update_row(row, request_data) {
  $.ajax({
    url:      'http://127.0.0.1:8000/finance/submitchangestable/',
    type:     'POST',
    data:     {request_data: JSON.stringify(request_data)},
    success:  function (response) {
                console.log('Successfully updated transaction ' + request_data.id + '\'s data.');

                // Have the row flash blue for a sucessfull update.
                var baseColor = row.css('background-color');
                row.animate({  backgroundColor: jQuery.Color('#aad1e0')}, 100 );
                row.animate({ backgroundColor: jQuery.Color(baseColor)}, 250);
              },
    error:    function (xhr,errmsg,err) {
                console.log('failure');
              }
  });
};





// Resets the transaction form to all blank values. Except date which is reset to
// the current date.
function clear_transaction_form() {
  // Traditional form value resets.
  $('#transaction-form #id_date').val('');
  $('#transaction-form #id_description').val('');
  $('#transaction-form #id_total').val('');
  $('#transaction-from #id_tax').val('');

  // Semantic-UI dropdown resets.
  $('#transaction-form #id_payment_method').dropdown('clear');
  $('#transaction-form #id_retailer').dropdown('clear');
  $('#transaction-form #id_categories').dropdown('clear');
}





// Obtains the current information entered into the transaction form.
function gather_transaction_form() {
  return {
    date:         $('#transaction-form #id_date').val(),
    description:  $('#transaction-form #id_description').val(),
    total:        $('#transaction-form #id_total').val(),
    tax:          $('#transaction-from #id_tax').val(),
    method:       gather_dropdown_info('#transaction-form #id_payment_method')[0],
    retailer:     gather_dropdown_info('#transaction-form #id_retailer')[0],
    categories:   gather_dropdown_info('#transaction-form #id_categories')
  }
}





// Obtains the current information of a specified dropdown (pass the html/css id to the
// function as the argument), formatted as an array of elements that are either an id
// of a pre-existing value or the name of one that needs to be created.
//
// If the value needs to be created  then only the name of the element to create will
// be given, otherwise the id of the element which already exists will only be given.
//
// Returns an array so that both multiple and non-multiple dropdown selects can be
// handled. Non-multiple dropdown selects return an array of length 1.
function gather_dropdown_info(target) {
  var value = $(target).dropdown('get value').slice(-1)[0];

  if (value instanceof Array) {
    var result = [];

    // Process all items and add them to result.
    for (i = 0; i < value.length; i++) {
      var cur_item = value[i];

      // Test if value needs to be created. If the value is NaN then it is text and thus
      // needs to be created, If it is a number, then it is the ID of an existing element.
      if (Number.isNaN(parseInt(cur_item))) {
        result.push(cur_item);
      } else {
        result.push(parseInt(cur_item));
      }
    }
    return result;
  } else {
    // Test if value needs to be created. If the value is NaN then it is text and thus
    // needs to be created, If it is a number, then it is the ID of an existing element.
    if (Number.isNaN(parseInt(value))) {
      return [value]
    } else {
      return [parseInt(value)]
    }
  }
}
