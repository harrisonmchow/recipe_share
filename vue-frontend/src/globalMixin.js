// globalMixin.js
import axios from "axios"

export default {
  methods: {
    redirect(endpoint) {
      // Your global method logic here
      this.$router.push(endpoint)
    },
    async checkForToken() {
      const token = this.getCookie('sss_token');
      if (!token) {
        this.hasToken = false;
        return;
      }
      console.log("Checking token");
      const db_host = import.meta.env.VITE_DB_HOST;
      try {
        const response = await axios.post(
          `${db_host}/validate_token`,
          {
            token: token
          },
          {
            headers: {
              "Content-type": "application/json",
              "Access-Control-Allow-Origin": "*"
            }
          }
        );
        this.hasToken = response.data.valid;
      } catch (err) {
        console.log(err);
        this.hasToken = false;
      }

    },
    getCookie(name) {
      const cookies = document.cookie.split('; ');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].split('=');
        if (cookie[0] === name) {
          return decodeURIComponent(cookie[1]);
        }
      }
      return null;
    },
  }
}