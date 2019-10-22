import store from "store";

const CURRENT_USER_STORE_KEY = "loggedInUser";

export async function storeCurrentUser(currentUser) {
  /* In case it fails
  notification.warning({
        message: error.code,
        description: error.message
      });
  */
  return new Promise(resolve => {
    setTimeout(() => {
      store.set(CURRENT_USER_STORE_KEY, currentUser);

      resolve(currentUser);
    }, 900);  // Remove this in production
  });
}


export async function loadUserFromStore() {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve(store.get(CURRENT_USER_STORE_KEY));
    }, 500);
  });
}

export async function clearUser() {
  store.remove(CURRENT_USER_STORE_KEY);
}
