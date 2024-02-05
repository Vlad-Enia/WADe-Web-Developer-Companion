export interface Authorization{
    access_token: string;
}

export interface Preference{
    owner_username: string;
    origins: Array<String>;
    topics: Array<String>;
}