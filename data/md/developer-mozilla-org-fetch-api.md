The Fetch API uses [`Request`](/en-US/docs/Web/API/Request) and [`Response`](/en-US/docs/Web/API/Response) objects (and other things involved with network requests), as well as related concepts such as CORS and the HTTP Origin header semantics.

For making a request and fetching a resource, use the [`fetch()`](/en-US/docs/Web/API/Window/fetch "fetch()") method. It is a global method in both [`Window`](/en-US/docs/Web/API/Window) and [`Worker`](/en-US/docs/Web/API/WorkerGlobalScope "Worker") contexts. This makes it available in pretty much any context you might want to fetch resources in.

The `fetch()` method takes one mandatory argument, the path to the resource you want to fetch. It returns a [`Promise`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) that resolves to the [`Response`](/en-US/docs/Web/API/Response) to that request â as soon as the server responds with headers â **even if the server response is an HTTP error status**. You can also optionally pass in an `init` options object as the second argument (see [`Request`](/en-US/docs/Web/API/Request)).

Once a [`Response`](/en-US/docs/Web/API/Response) is retrieved, there are a number of methods available to define what the body content is and how it should be handled.

You can create a request and response directly using the [`Request()`](/en-US/docs/Web/API/Request/Request "Request()") and [`Response()`](/en-US/docs/Web/API/Response/Response "Response()") constructors, but it's uncommon to do this directly. Instead, these are more likely to be created as results of other API actions (for example, [`FetchEvent.respondWith()`](/en-US/docs/Web/API/FetchEvent/respondWith) from service workers).

Find out more about using the Fetch API features in [Using Fetch](/en-US/docs/Web/API/Fetch_API/Using_Fetch).