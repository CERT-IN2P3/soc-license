SOC_LICENSE = {
  'diploma': {
    'uuid': '#soc-license-diploma-uuid',
    'signature': '#soc-license-diploma-signature',
    'sha512sum': '#soc-license-diploma-sha512sum',
    'unsign': {
      'btn': '#soc-license-diploma-unsign-btn',
      'firstname': '#soc-license-diploma-unsign-firstname',
      'lastname': '#soc-license-diploma-unsign-lastname',
      'level': '#soc-license-diploma-unsign-level',
      'date': '#soc-license-diploma-unsign-date',
    }
  }
}

class SocLicenseDiploma {
  constructor(url) {
    this.url = url;
    self = this;
    $(SOC_LICENSE['diploma']['unsign']['btn']).on('click', function() {
        self.unsign();
    })
  }

  sha512sum() {
    var self = this;
    $.ajaxSetup({
        headers: { "X-CSRFToken": self.csrftoken}
    })
    return $.ajax({
      url: this.url + 'diplomas/' + $(SOC_LICENSE['diploma']['uuid']).val() + '?format=sha512sum',
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
        $(SOC_LICENSE['diploma']['sha512sum']).val(data.sha512sum)
      }
    })
  }

  unsign() {
    var self = this;
    var data = {
        "uuid": $(SOC_LICENSE['diploma']["uuid"]).val(),
        "signature": $(SOC_LICENSE['diploma']['signature']).val()
    };
    $.ajaxSetup({
        headers: { "X-CSRFToken": self.csrftoken}
    })
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
        $(SOC_LICENSE['diploma']['unsign']['firstname']).val(data.firstname)
        $(SOC_LICENSE['diploma']['unsign']['lastname']).val(data.lastname)
        $(SOC_LICENSE['diploma']['unsign']['level']).val(data.level)
        $(SOC_LICENSE['diploma']['unsign']['date']).val(data.date)
      }
    })
  }

}
