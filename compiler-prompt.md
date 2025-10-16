Your job is to build and maintain a language-to-language compiler that translates source language code to target language code.

You have access to the compiler repository which includes the lexer, parser, semantic analyzer, and code generator components.

Make a commit and push your changes after every single file edit.

Use the .agent/ directory as a scratchpad for your work. Store long term plans, todo lists, and design documents there.

## Project Structure

The compiler should be organized into the following components:

- **Lexer/Tokenizer**: Breaks source code into tokens
- **Parser**: Builds an Abstract Syntax Tree (AST) from tokens
- **Semantic Analyzer**: Type checking, scope analysis, and validation
- **Code Generator**: Transforms AST into target language code
- **Runtime/Standard Library**: Support code needed for compiled output

## Development Workflow

1. **Implement incrementally**: Start with a minimal viable compiler for basic language features
2. **Test thoroughly**: Write tests for each compiler phase (lexer, parser, semantic analysis, code generation)
3. **Document as you go**: Keep documentation up-to-date with language specifications and compiler architecture

## Testing Strategy

The compiler should have comprehensive test coverage:

- **Unit tests**: Test individual compiler components (lexer rules, parser productions, etc.)
- **Integration tests**: Test full compilation pipeline for language features
- **End-to-end tests**: Compile and run complete programs, verify output correctness
- **Negative tests**: Verify proper error handling and error messages

A good heuristic is to spend 70% of your time on implementation and 30% on testing. Every new language feature should have corresponding tests.

## Language Feature Priority

Implement language features in this order:

1. **Core features**: Variables, basic types, expressions, control flow
2. **Functions**: Function definitions, calls, parameters, return values
3. **Advanced types**: Arrays, objects/structs, user-defined types
4. **Advanced features**: Closures, generics, modules, etc.

## Code Quality Standards

- Write clean, maintainable compiler code
- Use meaningful variable and function names
- Add comments for complex algorithms (especially in parser and code generator)
- Follow consistent code style throughout the project
- Optimize for correctness first, performance second

## Error Handling

The compiler should provide helpful error messages:

- Include source location (file, line, column)
- Explain what went wrong clearly
- Suggest possible fixes when applicable
- Use colors/formatting for readability (if terminal supports it)

## Documentation Requirements

Maintain the following documentation:

- **Language specification**: Formal grammar, type system, semantics
- **Architecture guide**: How the compiler works, component interactions
- **API documentation**: For any public APIs or libraries
- **Examples**: Sample programs in the source language with expected output
