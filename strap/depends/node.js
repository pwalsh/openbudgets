try {
    console.log(require.resolve("less"));
} catch(e) {
    console.error("LESS is not installed");
    process.exit(e.code);
}