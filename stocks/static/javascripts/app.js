// Angular app module

(function(){

  var app = angular.module('stockWatch',['stockWatch.routes','stockWatch.controllers',
    'stockWatch.services','angular-loading-bar', "stockWatch.directives","ngSanitize","chart.js"]);

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
  
})();