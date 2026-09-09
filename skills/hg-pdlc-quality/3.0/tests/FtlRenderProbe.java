import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateExceptionHandler;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;

/** Template syntax/branch probe only. Never executes shell, nodes, agents, or transitions. */
public final class FtlRenderProbe {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("Usage: FtlRenderProbe <fixtures-directory>");
        }
        Path dir = Path.of(args[0]).toAbsolutePath();
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_32);
        cfg.setDefaultEncoding("UTF-8");
        cfg.setTemplateExceptionHandler(TemplateExceptionHandler.RETHROW_HANDLER);
        cfg.setLogTemplateExceptions(false);
        cfg.setWrapUncheckedExceptions(true);
        cfg.setFallbackOnNullLoopVariable(false);
        var refPattern = Pattern.compile("step\\[\"([^\"]+)\"\\]");
        int rendered = 0;
        try (var stream = Files.list(dir)) {
            for (Path file : stream.filter(p -> p.toString().endsWith(".ftl")).sorted().toList()) {
                String source = Files.readString(file, StandardCharsets.UTF_8);
                Template template = new Template(file.getFileName().toString(), source, cfg);
                for (String mode : new String[]{"initial", "keep", "rollback"}) {
                    Map<String,Object> steps = new HashMap<>();
                    var refs = refPattern.matcher(source);
                    while (refs.find()) {
                        Map<String,Object> entry = new HashMap<>();
                        entry.put("attempt", 1);
                        entry.put("change_id", "CHG-probe-123456");
                        entry.put("status", "done");
                        entry.put("route", "on_approve");
                        if (!mode.equals("initial")) {
                            entry.put("rework_instruction", "PROBE-FEEDBACK: keep the original acceptance criterion.");
                            entry.put("keep_changes", mode.equals("keep"));
                            entry.put("basis_hash", "probe-basis-not-a-real-artifact");
                        }
                        steps.put(refs.group(1), entry);
                    }
                    Map<String,Object> data = new HashMap<>();
                    data.put("step", steps);
                    data.put("run", Map.of("feature_request", "Probe: quotes \" and newline\nare data, not a shell command."));
                    data.put("env", Map.of());
                    StringWriter result = new StringWriter();
                    template.process(data, result);
                    String output = result.toString();
                    if (source.contains("rework_instruction?has_content")) {
                        if (mode.equals("initial") && output.contains("PROBE-FEEDBACK")) {
                            throw new AssertionError(file + ": stale feedback on initial run");
                        }
                        if (!mode.equals("initial") && !output.contains("PROBE-FEEDBACK")) {
                            throw new AssertionError(file + ": feedback lost in " + mode);
                        }
                        if (source.contains("ДОРАБОТКА:") && mode.equals("keep") && !output.contains("ДОРАБОТКА:")) {
                            throw new AssertionError(file + ": keep branch missing");
                        }
                        if (source.contains("ПОВТОР ПОСЛЕ ОТКАТА:") && mode.equals("rollback") && !output.contains("ПОВТОР ПОСЛЕ ОТКАТА:")) {
                            throw new AssertionError(file + ": rollback branch missing");
                        }
                    }
                    rendered++;
                    System.out.println("PASS " + file.getFileName() + " mode=" + mode);
                }
            }
        }
        if (rendered == 0) throw new AssertionError("No templates found");
        System.out.println("Rendered " + rendered + " fixture cases. This is NOT a live HG execution.");
    }
}
