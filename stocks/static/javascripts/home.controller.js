// Home controllers

(function(){

  angular.module('stockWatch.controllers')
    .controller('homeController', homeController);

  homeController.$inject = ['$scope','Layout','$interval','$window','$timeout','$http','$rootScope','$state'];

  function homeController($scope,Layout, $interval,$window,$timeout,$http,$rootScope,$state){

    var vm = this;
    vm.ipo_data = [];

    Layout.get_ipo_data()
    .then(function successCallback(response){
      vm.ipo_data = response.data; 
    }, function failureCallback(response){

    });
  };
})();