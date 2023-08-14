SOC_LICENSE = {
  'banner': {
    'firstname': '#soc-license-banner-firstname',
    'lastname': '#soc-license-banner-lastname',
    'progress-bar': '#soc-license-banner-progress-bar',
    'progress-basic': '#soc-license-banner-progress-basic',
    'progress-advanced': '#soc-license-banner-progress-advanced',
    'progress-expert': '#soc-license-banner-progress-expert',
  },
  'init': {
    'name': '#soc-license-init',
    'firstname': '#soc-license-init-firstname',
    'lastname': '#soc-license-init-lastname',
    'lang': '#soc-license-init-lang',
    'start': '#soc-license-init-start',
    'close': '#soc-license-init-close',
  },
  'question': {
    'name': '#soc-license-question',
    'text': '#soc-license-question-text',
    'next': '#soc-license-question-next',
    'explanation': '#soc-license-question-explanation'
  },
  'answers': {
    'name': '#soc-license-answers',
    'submit': '#soc-license-answer-submit',
    'answer': '#soc-license-answer'
  },
  'diploma': {
    'name': '#soc-license-diploma',
    'header': '#soc-license-diploma-header',
    'text': '#soc-license-diploma-text',
    'link-json': '#soc-license-diploma-link-json',
    'link-pdf': '#soc-license-diploma-link-pdf',
    'score': '#soc-license-diploma-score',
  },
}


class SocLicenseExam {
  constructor(url) {
    this.url = url;
    this.result = {};
    this.question();
    this.csrftoken = Cookies.get('csrftoken')
    self = this;
    $(SOC_LICENSE['question']['next']).hide();
    $(SOC_LICENSE['init']['start']).on('click', function() {
        self.init();
    })
    $(SOC_LICENSE['answers']['submit']).on('click', function() {
        self.answer();
    })
    $(SOC_LICENSE['question']['next']).on('click', function() {
        self.question();
    })
    $(SOC_LICENSE['init']['close']).on('click', function() {
        self.close();
    })
    $(SOC_LICENSE['banner']['firstname']).text(Cookies.get("firstname"))
    $(SOC_LICENSE['banner']['lastname']).text(Cookies.get("lastname"))
    this.progress();
  }

  showStage(stage) {
    $(SOC_LICENSE['init']['name']).hide();
    $(SOC_LICENSE['question']['name']).hide();
    $(SOC_LICENSE['diploma']['name']).hide();
    if (stage == 'init') {
        $(SOC_LICENSE['init']['name']).show();
    }
    if (stage == 'question') {
        $(SOC_LICENSE['question']['name']).show();
    }
    if (stage == 'finished') {
        $(SOC_LICENSE['diploma']['name']).show();
    }
  }

  init() {
    var data = {
        'firstname': $(SOC_LICENSE['init']['firstname']).val(),
        'lastname': $(SOC_LICENSE['init']['lastname']).val(),
        'lang': $(SOC_LICENSE['init']['lang']).val()
    }
    var self = this;
    Cookies.set('firstname', data.firstname, { expires: 1, sameSite: 'None', secure: true })
    Cookies.set('lastname', data.lastname, { expires: 1, sameSite: 'None', secure: true })

    $(SOC_LICENSE['banner']['firstname']).text(Cookies.get("firstname"))
    $(SOC_LICENSE['banner']['lastname']).text(Cookies.get("lastname"))

    $.ajaxSetup({
        headers: { "X-CSRFToken": self.csrftoken}
    })
    $.ajax({
      url: this.url + 'exams/init/',
      type: 'POST',
      crossDomain: true,
      dataType: 'json',
      data: JSON.stringify(data),
       xhrFields: {
          withCredentials: true
       },
      header: {
        'Access-Control-Allow-Credentials' : true,
        'Access-Control-Allow-Methods':'POST',
        'Access-Control-Allow-Headers':'application/json',
        },
      success: function(data){
        console.log(data)
        self.showStage(data.stage);
        self.result = data;

        Cookies.set('score', 0, { expires: 1, sameSite: 'None', secure: true })
        Cookies.set('basic', data.basic, { expires: 1, sameSite: 'None', secure: true })
        Cookies.set('advanced', data.advanced, { expires: 1, sameSite: 'None', secure: true })
        Cookies.set('expert', data.expert, { expires: 1, sameSite: 'None', secure: true })
        self.progress();
        self.question();
      }
    })
  }

  question() {
    var self = this;
    $.ajaxSetup({
        headers: { "X-CSRFToken": self.csrftoken}
    })
    return $.ajax({
      url: this.url + 'exams/questions/',
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
        var answers = "";
        self.showStage(data.stage);
        if (data.stage == 'finished') {
            $("#soc-license-score").text(data.score)
            if (data.status == 'success') {
                $(SOC_LICENSE['diploma']['header']).text('Félicitations !');
                $(SOC_LICENSE['diploma']['link-json']).attr("href", self.url +
                                                    'diplomas/' + data.uuid +
                                                    '.json');
                $(SOC_LICENSE['diploma']['link-pdf']).attr("href", self.url +
                                                    'diplomas/' + data.uuid +
                                                    '.pdf');
                $(SOC_LICENSE['diploma']['text']).show();
            } else {
                $(SOC_LICENSE['diploma']['header']).text('Désolé ,')
                $(SOC_LICENSE['diploma']['text']).hide();
            }
        } else {
            $(SOC_LICENSE['question']['text']).text(data.text)
            $.each(data.answers, function(index, answer){
                answers += '<div class="form-check">';
                answers += '<input value="' + answer['id'] + '" id="' + answer['id'] +
                           '" name="' + SOC_LICENSE['answers']['answer'] +
                           '" type="radio" class="form-check-input" required>'
                answers += '<label class="form-check-label" for="' + answer['id'] + '">' + answer['text'] + '</label>'
                answers += '</div>';
            })
            $(SOC_LICENSE['question']['next']).hide();
            $(SOC_LICENSE['question']['explanation']).hide();

            $(SOC_LICENSE['answers']['name']).html(answers);
            $(SOC_LICENSE['answers']['submit']).show();
        }
        self.result = data;
      }
    })
  }

  answer() {
    var self = this;
    var data = {
        'answer': $('input[name="' + SOC_LICENSE['answers']['answer'] + '"]:checked').val()
    }
    console.log(data)
    $.ajaxSetup({
        headers: { "X-CSRFToken": self.csrftoken}
    })
    return $.ajax({
      url: this.url + 'exams/questions/' + self.result['question'],
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
        console.log(data);
        self.result = data;
        if (data.point == 0) {
          $(SOC_LICENSE['question']['explanation']).removeClass('alert-success')
          $(SOC_LICENSE['question']['explanation']).addClass('alert-danger')
        } else {
          $(SOC_LICENSE['question']['explanation']).removeClass('alert-danger')
          $(SOC_LICENSE['question']['explanation']).addClass('alert-success')
        };
        $(SOC_LICENSE['question']['explanation']).text(data.explanation);
        $(SOC_LICENSE['question']['explanation']).show();
        $(SOC_LICENSE['question']['next']).show();

        $(SOC_LICENSE['answers']['submit']).hide();
        Cookies.set('score', data.score, { sameSite: 'None', secure: true})
        self.progress()
      }
    })
  }

  close() {
    var self = this;
    $.ajaxSetup({
        headers: { "X-CSRFToken": self.csrftoken}
    })
    return $.ajax({
      url: this.url + 'exams/init/',
      type: 'DELETE',
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
        console.log(data);
        self.result = data;
        self.showStage(data.stage);

        Cookies.remove('firstname')
        Cookies.remove('lastname')
        Cookies.remove('basic')
        Cookies.remove('advanced')
        Cookies.remove('expert')
        Cookies.remove('score')
      }
    })
  }

  progress() {
    if (Number(Cookies.get('score')) <= Number(Cookies.get('basic'))) {
        $(SOC_LICENSE['banner']['progress-basic']).css('width',
          Cookies.get('score') * 100 / Cookies.get('expert') + '%')
        $(SOC_LICENSE['banner']['progress-advanced']).css('width', '0%')
        $(SOC_LICENSE['banner']['progress-expert']).css('width', '0%')
    } else {
        $(SOC_LICENSE['banner']['progress-basic']).css('width',
          Cookies.get('basic') * 100 / Cookies.get('expert') + '%')
        if (Number(Cookies.get('score')) <= Number(Cookies.get('advanced'))) {
            $(SOC_LICENSE['banner']['progress-advanced']).css('width',
              (Cookies.get('score') - Cookies.get('basic')) * 100 / Cookies.get('expert') + '%')
            $(SOC_LICENSE['banner']['progress-expert']).css('width', '0%')
        } else {
            $(SOC_LICENSE['banner']['progress-advanced']).css('width',
              (Cookies.get('advanced') - Cookies.get('basic')) * 100 / Cookies.get('expert') + '%')
            $(SOC_LICENSE['banner']['progress-expert']).css('width',
              (Cookies.get('score') - Cookies.get('advanced')) * 100 / Cookies.get('expert') + '%')
        }
    }
  }

  diploma() {
  return $.ajax({
      url: this.url + 'diplomas/',
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
        }
    })
  }

}
