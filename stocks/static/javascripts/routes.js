// Angular routes

(function(){

  angular.module('stockWatch.routes')
  .config(function($stateProvider, $urlRouterProvider,$locationProvider) {
    
    // For any unmatched url, redirect to /state1
    //$urlRouterProvider.otherwise("/accounts");
    //
    // Now set up the states
    $stateProvider
      .state('home', {
        url: "/",
        templateUrl: "/static/partials/homepage.html",
        params: { first_name: null, email: null},
        controller: "indexController",
        controllerAs: 'vm'
      })
      .state('login',{
        url: "/accounts",
        templateUrl: "/static/login/partials/login_signup.html",
        controller: "accountsController",
        controllerAs: 'vm'
      })
      .state('company',{
        url: "/company/:name",
        templateUrl: "/static/partials/company.html",
        params: { id: null },
        controller: "companyDetailsController",
        controllerAs: 'vm'
      });

    $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });
    $locationProvider.hashPrefix('!');
  });

})();