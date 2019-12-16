$( document ).ready(function() {
  Vue.component('history-tab', {
    props: ['match'],
    template: '<div class="history-tab"><div class="info">{{match.champion}}</div> <div class="info">Kills: {{match.k}}</div> <div class="info">Deaths: {{match.d}}</div> <div class="info">Assists: {{match.a}}</div> <div class="info">Win: {{match.win}}</div></div>'
  });

  var app = new Vue({
    delimiters: ['${', '}'],
    el: '#app',
    data: {
      searchState: true,
      message: '',
      query: '',
      matches: [],
      apiKey: ''
    },
    methods: {
      searchSummoner: function () {
        $(".search_btn_icon").removeClass("fa-search").addClass("fa-spinner");
        var me = this;
        $.ajax({
          url: "/matchHistory/" + this.query + (this.apiKey ? '/'+this.apiKey : ''),
          method: "GET",
          async: true,
          dataType: 'json',
          success: function(res) {
            me.matches = res;
            me.searchState = false;
          },
          error: function() {
            me.message = "Look up failed. Try another sumonner's name or use a valid API Key."
          }
        })
      },
      back: function() {
        this.searchState = true;
      }
    }
  });
});
