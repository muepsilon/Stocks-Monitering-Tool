(function(){

  angular.module('stockWatch.controllers')
    .controller('accountsController', accountsController);

  accountsController.$inject = ['$scope','Layout','$stateParams','$cookies','$state'];

  function accountsController($scope,Layout, $stateParams,$cookies,$state){

    var vm = this;
    vm.showpage = false;
    vm.is_logged_in = false;
    vm.login = login;
    vm.signup = signup;
    vm.formdata = {
      "signup" : {
        "firstName" : "",
        "lastName": "",
        "email": "",
        "username": "",
        "password": ""
      },
      "login":{
        "email": "",
        "password": ""
      }
    }
    vm.formselect = "login";

    Layout.is_logged_in()
      .then(function(response){
      console.log(response.data);
        if (response.data.login == true) {
          $state.go("home",{first_name: response.data.first_name, email: response.data.email});
        } else {
          vm.is_logged_in = false;
        }
        vm.showpage = true;
      });
    function login () {
      Layout.login(vm.formdata.login)
      .then(function success(response){
        console.log(response);
      }, function failure(response){
        console.log(response);
      });
    }

    function signup () {
      // body...
    }
  };
})();