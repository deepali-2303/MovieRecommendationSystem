<script>
  let username = '';
  let email = '';
  let password = '';
  let message = '';

  const handleSignup = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });

      if (response.ok) {
        message = 'Signup successful!';
        // Optionally redirect to login
        setTimeout(() => {
          window.location.href = '/login';
        }, 2000);
      } else {
        const error = await response.json();
        message = `Error: ${error.message || 'Signup failed'}`;
      }
    } catch (err) {
      message = 'Error: Unable to connect to the server.';
    }
  };
</script>

<style>
  body {
    margin: 0;
    font-family: 'Helvetica', sans-serif;
    background-color: #141414; /* Dark background */
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }

  form {
    display: flex;
    flex-direction: column;
    max-width: 400px;
    width: 100%;
    padding: 40px;
    border-radius: 8px;
    background-color: rgba(0, 0, 0, 0.8); /* Subtle dark transparent background */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  }

  h2 {
    font-size: 28px;
    margin-bottom: 20px;
    text-align: center;
  }

  input {
    margin-bottom: 15px;
    padding: 15px;
    font-size: 16px;
    border: 1px solid #444; /* Softer gray border */
    border-radius: 4px;
    background-color: #333; /* Dark input background */
    color: white;
    outline: none;
    transition: background-color 0.3s ease;
  }

  input:focus {
    background-color: #555; /* Slightly lighter on focus */
  }

  button {
    padding: 15px;
    font-size: 18px;
    cursor: pointer;
    background-color: #4CAF50; /* Subtle green */
    color: white;
    border: none;
    border-radius: 4px;
    margin-top: 10px;
    transition: background-color 0.3s ease;
  }

  button:hover {
    background-color: #45a049; /* Darker green on hover */
  }

  p {
    margin-top: 15px;
    text-align: center;
  }

  p.error {
    color: #e50914; /* Red for errors */
  }

  p.success {
    color: #21c00c; /* Green for success */
  }
</style>

<form on:submit|preventDefault={handleSignup}>
  <h2>Signup</h2>
  <input
    type="text"
    bind:value={username}
    placeholder="Username"
    required
  />
  <input
    type="email"
    bind:value={email}
    placeholder="Email"
    required
  />
  <input
    type="password"
    bind:value={password}
    placeholder="Password"
    required
  />
  <button type="submit">Sign Up</button>

  {#if message}
    <p class="{message.startsWith('Error') ? 'error' : 'success'}">{message}</p>
  {/if}
</form>
