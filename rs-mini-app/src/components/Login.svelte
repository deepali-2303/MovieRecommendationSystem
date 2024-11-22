<script>
  let username = '';
  let password = '';
  let errorMessage = '';
  let token = null;

  const loginUser = async () => {
      try {
          const response = await fetch('http://127.0.0.1:5000/login', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ username, password }),
          });

          if (!response.ok) {
              throw new Error('Login failed');
          }

          const data = await response.json();
          token = data.token;  // Assuming 'token' is part of the response

          // Store the token in localStorage
          if (token) {
              localStorage.setItem('jwt_token', token);
              console.log('Token stored in localStorage!');
          }

      } catch (error) {
          errorMessage = error.message;
          console.error('Error:', errorMessage);
      }
  };
</script>

<div>
  <input type="text" bind:value={username} placeholder="Username" />
  <input type="password" bind:value={password} placeholder="Password" />
  <button on:click={loginUser}>Login</button>

  {#if errorMessage}
      <p>{errorMessage}</p>
  {/if}
</div>
