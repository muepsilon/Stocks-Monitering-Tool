// Home controllers

(function(){

  angular.module('stockWatch.controllers')
    .controller('homeController', homeController);

  homeController.$inject = ['$scope','Layout','$interval','$window','$timeout','$http','$rootScope','$state'];

  function homeController($scope,Layout, $interval,$window,$timeout,$http,$rootScope,$state){

    var vm = this;
    vm.ipo_data = [];
    vm.indices = [];
    index_list = ["nifty_50", "nifty_midcap_50","nifty_sml100_free","nifty_500"];
    vm.index_keys = ["last","previousClose","yearHigh","yearLow"]

    Layout.get_ipo_data()
    .then(function successCallback(response){
      vm.ipo_data = response.data; 
    }, function failureCallback(response){

    });
    Layout.get_indices()
    .then(function(response){
      if (response.data !== null) {
        index_data = response.data;
        for (index in index_list){
          if (index_list[index] in index_data){
            vm.indices.push(index_data[index_list[index]]);
          }
        }
      };
    });
  };
})();