class SocLicense {
  constructor(url) {
    this.url = url;
    this.result = {};
    this.question();
    self = this;
    $('#soc-license-next-question').hide();
    $('#soc-license-start').on('click', function() {
        self.init();
    })
    $('#soc-license-answer-submit').on('click', function() {
        self.answer();
    })
    $('#soc-license-next-question').on('click', function() {
        self.question();
    })
    $('#soc-license-close').on('click', function() {
        self.close();
    })
  }

  showStage(stage) {
    $('#soc-license-init').hide();
    $('#soc-license-question').hide();
    $('#soc-license-result').hide();
    if (stage == 'init') {
        $('#soc-license-init').show();
    }
    if (stage == 'question') {
        $('#soc-license-question').show();
    }
    if (stage == 'finished') {
        $('#soc-license-result').show();
    }
  }

  init() {
    var data = {
        'firstname': $('#firstName').val(),
        'lastname': $('#lastName').val(),
        'lang': $('#language').val()
    }
    var self = this;
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
        self.showStage(data.stage);
        self.result = data;
        self.question();
      }
    })
  }

  question() {
    var self = this;
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
                $('#soc-license-result-header').text('Félicitations !');
                $('#soc-license-diploma-link').attr("href", self.url + 'diplomas/' + data.uuid + '.pdf');
                $('#soc-license-result-body').show();
            } else {
                $('#soc-license-result-header').text('Désolé ,')
                $('#soc-license-result-body').hide();
            }
        } else {
            $('#soc-license-question-text').text(data.text)
            $.each(data.answers, function(index, answer){
                answers += '<div class="form-check">';
                answers += '<input value="' + answer['id'] + '" id="' + answer['id'] + '" name="soc-license-question-answer" type="radio" class="form-check-input" required>'
                answers += '<label class="form-check-label" for="' + answer['id'] + '">' + answer['text'] + '</label>'
                answers += '</div>';
            })
            $('#soc-license-answer-submit').show();
            $('#soc-license-next-question').hide();
            $('#soc-license-explanation').hide();
            $('#soc-license-question-answers').html(answers);
        }
        self.result = data;
      }
    })
  }

  answer() {
    var self = this;
    var data = {
        'answer': $('input[name="soc-license-question-answer"]:checked').val()
    }
    console.log(data)
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
          $('#soc-license-explanation').removeClass('alert-success')
          $('#soc-license-explanation').addClass('alert-danger')
        } else {
          $('#soc-license-explanation').removeClass('alert-danger')
          $('#soc-license-explanation').addClass('alert-success')
        };
        $('#soc-license-answer-submit').hide();
        $('#soc-license-explanation').text(data.explanation);
        $('#soc-license-explanation').show();
        $('#soc-license-next-question').show();
      }
    })
  }

  close() {
    var self = this;
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
      }
    })
  }

}
