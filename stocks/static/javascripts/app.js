// Angular app module

(function(){

  var app = angular.module('stockWatch',['chart.js','stockWatch.routes','stockWatch.controllers',
    'stockWatch.services','angular-loading-bar', "stockWatch.directives","ngSanitize",'ui.bootstrap']);

  angular.module('stockWatch.routes',['ui.router']);

  angular.module('stockWatch.controllers',['ngCookies']);

  angular.module('stockWatch.directives',[]);

  app.config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.withCredentials = true;
  });
  
  app.filter('spaceless',function() {
    return function(input) {
        if (input) {
            return input.replace(/\s+/g, '-');    
        }
    }
  });

  app.filter('regularForm',function() {
    return function(input) {
        if (input) {
            return input.replace(/([A-Z])/g, ' $1').replace(/^./, function(str){ return str.toUpperCase(); });    
        }
    }
  });
  app.filter('shortName',function(){
    return function(name,length){
      var shortname = "";
      var maxLength = length == undefined ? 25 : length;
      name = name.replace("Limited","");
      name = name.replace("limited","");
      if (name.length > maxLength) {
        names = name.split(" ");
        index = 0;
        while(shortname.length < maxLength && index < names.length){
          shortname+=names[index]+" ";
          index+=1;
        }
      } else {
        shortname = name;
      }
      return shortname;
    }
  });
  
})();