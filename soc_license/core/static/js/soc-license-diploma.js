class SocLicenseDiploma {
  constructor(url) {
    this.url = url;
    self = this;
    $('#soc-license-diploma-uuid-btn').on('click', function() {
        self.sha512sum();
    })
    $('#soc-license-diploma-unsign-btn').on('click', function() {
        self.unsign();
    })
  }

  sha512sum() {
    var self = this;
    return $.ajax({
      url: this.url + 'diplomas/' + $('#soc-license-diploma-uuid').val(),
      type: 'GET',
      crossDomain: true,
      dataType: 'json',
       xhrFields: {
          withCredentials: true
       },
      header: {
        'Access-Control-Allow-Credentials' : true,
        'Access-Control-Allow-Methods':'GET',
        'Access-Control-Allow-Headers':'application/json',
        },
      success: function(data){
        console.log(data)
        $('#soc-license-sha512sum').val(data.sha512sum)
      }
    })
  }

  unsign() {
    var self = this;
    var data = {
        "signature": $('#soc-license-diploma-sign').val()
    };
    return $.ajax({
      url: this.url + 'diplomas/',
      type: 'POST',
      crossDomain: true,
      data: JSON.stringify(data),
      dataType: 'json',
       xhrFields: {
          withCredentials: true
       },
      header: {
        'Access-Control-Allow-Credentials' : true,
        'Access-Control-Allow-Methods':'GET',
        'Access-Control-Allow-Headers':'application/json',
        },
      success: function(data){
        console.log(data)
        $('#soc-license-diploma-unsign-firstname').val(data.firstname)
        $('#soc-license-diploma-unsign-lastname').val(data.lastname)
        $('#soc-license-diploma-unsign-score').val(data.score)
        $('#soc-license-diploma-unsign-date').val(data.date)
        $('#soc-license-diploma-uuid').val(data.uuid)
      }
    })
  }

}
