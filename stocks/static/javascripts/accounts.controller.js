(function(){

  angular.module('stockWatch.controllers')
    .controller('accountsController', accountsController);

  accountsController.$inject = ['$scope','Layout','$stateParams','$cookies','$state'];

  function accountsController($scope,Layout, $stateParams,$cookies,$state){

    var vm = this;
    vm.showpage = false;
    vm.error = {"signup": {"username": false, "email": false }, "login": false };
    vm.errormsg = "";
    vm.clearErrorMsgs = clearErrorMsgs;
    vm.errorMsgDuration = 2000; 
    vm.is_logged_in = false;
    vm.login = login;
    vm.signup = signup;
    vm.formdata = {
      "signup" : {
        "first_name" : "",
        "last_name": "",
        "email": "",
        "username": "",
        "password": ""
      },
      "login":{
        "username_email": "",
        "password": ""
      }
    }
    vm.formselect = $stateParams['form'] || "login";

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
        if($stateParams.redirect_state){
          if ($stateParams.redirect_state == 'company') {
            $state.go('company',{'name': $stateParams.endpoint});
          } else {
            $state.go('home')
          }
        } else {
          $state.go('home');
        }
      }, function failure(response){
        
      });
    }
    function clearErrorMsgs(){
      vm.error = {"signup": {"username": false, "email": false }, "login": false };
      $scope.$apply();
    }
    function signup () {
      Layout.duplicateCheck({'username' : vm.formdata.signup.username,'email': vm.formdata.signup.email})
      .then(function successCallback(response){
        if (response.data.username_taken == false && response.data.email_taken == false) {
          Layout.signup(vm.formdata.signup)
          .then(function success(response){
            console.log(response);

            if($stateParams.redirect_state){
              if ($stateParams.redirect_state == 'company') {
                $state.go('company',{'name': $stateParams.endpoint});
              } else {
                $state.go('home')
              }
            } else {
              $state.go('home');
            }
          }, function failure(response){
            console.log(response);
          });
        } else {
          if (response.data.username_taken) {
            vm.error.signup.username = true;
          }else{
            vm.error.signup.email = true;
          }
          setTimeout(vm.clearErrorMsgs,vm.errorMsgDuration);
        }
      },function failureCallback(response){

      });
      
    }
  };
})();