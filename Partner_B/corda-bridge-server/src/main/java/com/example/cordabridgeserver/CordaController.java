package com.example.cordabridgeserver;

import net.corda.client.rpc.CordaRPCClient;
import net.corda.client.rpc.CordaRPCConnection;
import net.corda.core.flows.FlowLogic;
import net.corda.core.messaging.CordaRPCOps;
import net.corda.core.utilities.NetworkHostAndPort;
import org.springframework.web.bind.annotation.*;

import java.io.File;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class CordaController {

    @PostMapping("/recordProof")
    public String recordProof(@RequestBody Map<String, String> payload) {
        String caseId = payload.get("case_id");
        String artifactId = payload.get("artifact_id");
        String documentHash = payload.get("document_hash");
        String documentType = payload.get("document_type");
        String createdAt = payload.get("created_at");

        // Make sure this matches the port in your PartyA window!
        NetworkHostAndPort nodeAddress = NetworkHostAndPort.parse("localhost:10006");
        CordaRPCClient client = new CordaRPCClient(nodeAddress);

        try {
            CordaRPCConnection connection = client.start("user1", "test");
            CordaRPCOps proxy = connection.getProxy();

            // 1. Manually load the JAR file from your hard drive
            File jarFile = new File("C:/Corda/cordapp-template-java/workflows/build/libs/workflows-0.1.jar");
            URLClassLoader classLoader = new URLClassLoader(new URL[]{jarFile.toURI().toURL()}, this.getClass().getClassLoader());

            // 2. Load the class using our custom classloader
            Class<?> flowClass = classLoader.loadClass("com.template.flows.RecordProofFlow");

            // 3. Start the flow dynamically
            String txId = (String) proxy.startFlowDynamic(
                    (Class<? extends FlowLogic<?>>) flowClass,
                    caseId, artifactId, documentHash, documentType, createdAt
            ).getReturnValue().get();

            connection.close();
            return "{\"status\":\"success\", \"transaction_id\":\"" + txId + "\"}";

        } catch (Exception e) {
            e.printStackTrace();
            return "{\"status\":\"error\", \"message\":\"" + e.getMessage() + "\"}";
        }
    }
}