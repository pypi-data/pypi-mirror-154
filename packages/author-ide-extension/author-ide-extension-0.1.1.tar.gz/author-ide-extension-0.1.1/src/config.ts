export const ATLAS_BASE_URL = (): string => {
  const currentURL = window.location.href;

  const params = new URL(currentURL).searchParams;
  const base_url: string | null = params.get('atlas_base_url');
  if (base_url === null) {
    return process.env.ATLAS_BASE_URL ??
      'https://author.skills.network/atlas'
  }

  return base_url;
};

/**
 * Extracts the session token. Will first try to get a token via the URL, if none was found then try to get the token via cookie
 *
 * @returns token
 */
export const ATLAS_TOKEN = (): string => {
  const currentURL = window.location.href;
  console.log('current URL is ', currentURL);

  const params = new URL(currentURL).searchParams;
  let token: string | null = params.get('token');
  console.log('Tried to get token from URL param - found:', token);
  if (token === null) {
    // try getting it from cookie
    const COOKIE_NAME: string = process.env.ATLAS_TOKEN_COOKIE_NAME ?? 'atlas_token';
    const reg: RegExp = new RegExp(`(^| )${COOKIE_NAME}=([^;]+)`);
    let match = reg.exec(document.cookie);
    if (match === null){
      throw Error('Invalid token');
    }
  token = match[2]
  console.log('Tried to get token from cookies - found:', token)
  }
  return token;
};
