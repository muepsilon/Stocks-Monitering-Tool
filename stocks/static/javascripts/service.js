// Angular services

(function(){

  angular.module('stockWatch.services',[])
    .factory('Layout',Layout);

    Layout.$inject = ['$http'];

    function Layout($http){

      var BASE_URL = "http://localhost:8000/";

      var Layout = {
        get_stocks :      get_stocks,
        delete_stock:     delete_stock,
        validate_company_name:  validate_company_name,
        add_stock:        add_stock,
        is_logged_in:     is_logged_in,
        edit_stock:       edit_stock,
        login:            login,
        signup:           signup,
        logout:           logout 
      };

      return Layout;

      function get_stocks(){
        return $http.get(BASE_URL + "api/latestprice/stocks");
      }

      function delete_stock(id){
        return $http.delete(BASE_URL + "api/stocks/" + id.toString());
      }

      function validate_company_name(query){
        return $http.get(BASE_URL + "api/company/find/?query=" + query)
        .success(function(){
        });
      }

      function add_stock(data){
        return $http.post(BASE_URL + "api/stocks/",data);
      }

      function edit_stock(id, data){
        return $http.put(BASE_URL + "api/stocks/" + id.toString(), data);
      }

      function login (data) {
        return $http.post(BASE_URL + "api/accounts/login/", data)
      }
      function signup (data) {
        return $http.post(BASE_URL + "api/accounts/signup/", data)
      }
      function logout () {
        return $http.post(BASE_URL + "api/accounts/logout/")
      }
      function is_logged_in(){
        return $http.post(BASE_URL + "api/accounts/verifysession/")
      }
    };

})();