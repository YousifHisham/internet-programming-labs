const express = require("express");
const app = express();
app.use(express.json());

// Allow requests from the React frontend
app.use((req, res, next) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    next();
});

let posts = [];
let nextPostId = 1;
let nextCommentId = 1;

// GET /posts - get all posts
app.get("/posts", (req, res) => {
    res.json(posts.map(({ comments, ...post }) => post));
});

// POST /posts - create a post
app.post("/posts", (req, res) => {
    const { name, content } = req.body;
    const post = { id: nextPostId++, name, content, comments: [] };
    posts.push(post);
    res.status(201).json({ id: post.id, name: post.name, content: post.content });
});

// GET /posts/:id - get a single post
app.get("/posts/:id", (req, res) => {
    const post = posts.find(p => p.id === parseInt(req.params.id));
    if (!post) return res.status(404).json({ error: "Post not found" });
    res.json({ id: post.id, name: post.name, content: post.content });
});

// PUT /posts/:id - edit a post
app.put("/posts/:id", (req, res) => {
    const post = posts.find(p => p.id === parseInt(req.params.id));
    if (!post) return res.status(404).json({ error: "Post not found" });
    if (req.body.name) post.name = req.body.name;
    if (req.body.content) post.content = req.body.content;
    res.json({ id: post.id, name: post.name, content: post.content });
});

// DELETE /posts/:id - delete a post
app.delete("/posts/:id", (req, res) => {
    const index = posts.findIndex(p => p.id === parseInt(req.params.id));
    if (index === -1) return res.status(404).json({ error: "Post not found" });
    posts.splice(index, 1);
    res.status(204).end();
});

// GET /posts/:id/comments - get post comments
app.get("/posts/:id/comments", (req, res) => {
    const post = posts.find(p => p.id === parseInt(req.params.id));
    if (!post) return res.status(404).json({ error: "Post not found" });
    res.json(post.comments.map(c => c.text));
});

// POST /posts/:id/comments - add a comment
app.post("/posts/:id/comments", (req, res) => {
    const post = posts.find(p => p.id === parseInt(req.params.id));
    if (!post) return res.status(404).json({ error: "Post not found" });
    const comment = { id: nextCommentId++, text: req.body.text };
    post.comments.push(comment);
    res.status(201).json(comment);
});

app.listen(4000, () => {
    console.log("Server running on http://localhost:4000");
});
